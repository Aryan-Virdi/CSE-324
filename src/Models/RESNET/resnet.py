"""Computer vision Regression pipeline based on ResNet for carrot count estimation."""
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, Subset
from torchvision import models, transforms
from PIL import Image
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from augment_image import batch_augment

#image transformation parameters derived from ResNet18 pretrained weights to ensure input normalization matches training conditions
RESNET18_WEIGHTS = models.ResNet18_Weights.DEFAULT
RESNET18_NORMALIZE_MEAN = RESNET18_WEIGHTS.transforms().mean
RESNET18_NORMALIZE_STD = RESNET18_WEIGHTS.transforms().std

# Paths for model output and weights - these are used both in training and inference to ensure consistency in where the model checkpoint is saved and loaded from
MODEL_OUTPUT_DIR = os.path.join("data", "Outputs")
MODEL_WEIGHTS_PATH = os.path.join(MODEL_OUTPUT_DIR, "plant_regressor_best.pth")


def build_resnet_transform():
    """Builds the image transformation pipeline for ResNet, including resizing, tensor conversion, and normalization.
    The images are resized to 224x224 pixels, converted to PyTorch tensors, and normalized using the mean and standard deviation values specific to ResNet18's pretrained weights."""
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=RESNET18_NORMALIZE_MEAN, std=RESNET18_NORMALIZE_STD)
    ])

class PlantCountDataset(Dataset):
    """Custom Dataset for Plant Counting with support for original, split, augmented, and blank images."""

    def __init__(self, csv_path, image_dir, transform=None):
        """Initializes the dataset by reading the CSV and preparing a list of samples."""
        self.df = pd.read_csv(csv_path)
        self.image_dir = image_dir
        self.transform = transform
        self.samples = []
        self._prepare_samples()

    def _prepare_samples(self):
        """Prepares the list of samples by combining original, split, augmented, and blank images."""
        original_sample_count = 0
        augmented_added = 0
        augmented_scanned = 0
        augmented_skipped_no_label = 0

        # Materialize one blank image once and append a matching virtual row.
        blank_stem = "__blank_train__"
        blank_path = os.path.join(self.image_dir, f"{blank_stem}.jpg")
        if not os.path.exists(blank_path):
            Image.new('RGB', (224, 224), (0, 0, 0)).save(blank_path)

        working_df = pd.concat([
            self.df,
            pd.DataFrame([{
                'file_name': blank_stem,
                'whole_count': 0.0,
                'left_count': 0.0,
                'right_count': 0.0,
            }]),
        ], ignore_index=True)

        def add_split_samples(img_path, label_row, sample_id_prefix, base_id):
            """Adds the original full image and its left/right splits as separate samples with appropriate labels."""
            self.samples.append({'path': img_path, 'label': label_row['whole_count'], 'id': f"{sample_id_prefix}_whole", 'base_id': base_id, 'type': 'full'})
            self.samples.append({'path': img_path, 'label': label_row['left_count'], 'id': f"{sample_id_prefix}_left", 'base_id': base_id, 'type': 'left'})
            self.samples.append({'path': img_path, 'label': label_row['right_count'], 'id': f"{sample_id_prefix}_right", 'base_id': base_id, 'type': 'right'})

        # 1. Add actual data from CSV plus one synthetic dataframe row for the blank sample
        for _, row in working_df.iterrows():
            fname = str(row['file_name']).strip()
            img_path = os.path.join(self.image_dir, f"{fname}.jpg")
            if fname == blank_stem:
                self.samples.append({'path': img_path, 'label': 0.0, 'id': 'blank_0', 'base_id': 'blank_train', 'type': 'full'})
                original_sample_count += 1
            else:
                add_split_samples(img_path, row, fname, fname)
                original_sample_count += 3

        # 2. Add augmented images using only whole_count (no left/right split).
        # Augmented files are expected to look like: <file_name>_aug_<n>.jpg
        augmented_dir = os.path.join(self.image_dir, "augmented")
        if os.path.isdir(augmented_dir):
            label_lookup = {
                str(row['file_name']).strip(): row
                for _, row in self.df.iterrows()
            }

            for filename in os.listdir(augmented_dir):
                if not filename.lower().endswith((".jpg", ".jpeg")):
                    continue
                augmented_scanned += 1

                stem = os.path.splitext(filename)[0]
                if "_aug_" not in stem:
                    continue

                base_id = stem.rsplit("_aug_", 1)[0]
                if base_id not in label_lookup:
                    augmented_skipped_no_label += 1
                    continue

                aug_path = os.path.join(augmented_dir, filename)
                self.samples.append({
                    'path': aug_path,
                    'label': label_lookup[base_id]['whole_count'],
                    'id': f"{stem}_whole",
                    'base_id': base_id,
                    'type': 'full'
                })
                augmented_added += 1

        print(
            "[Dataset] originals="
            f"{original_sample_count}, "
            f"aug_scanned={augmented_scanned}, "
            f"aug_added={augmented_added}, "
            f"aug_skip_no_label={augmented_skipped_no_label}"
        )
        
        print(f"[Dataset] total_samples={len(self.samples)}")

    def __len__(self): 
        return len(self.samples)

    def __getitem__(self, idx):
        """Returns the image tensor, label, and sample ID for the given index. Allows for use of squre bracket notation to get samples."""
        sample = self.samples[idx]
        image = Image.open(sample['path']).convert("RGB")
        w, h = image.size
        if sample['type'] == 'left': 
            image = image.crop((0, 0, w // 2, h))
        elif sample['type'] == 'right': 
            image = image.crop((w // 2, 0, w, h))
        
        label = torch.tensor([sample['label']], dtype=torch.float32)
        if self.transform: 
            image = self.transform(image)
        return image, label, sample['id']

def evaluate_model(model, loader, device, silent=False):
    """Evaluates the model on the given DataLoader and returns performance metrics. If silent=False, prints detailed results.
    The results include MAE, RMSE, and R2 score, along with a breakdown of predictions vs actuals for each sample.
    The MAE is calculated as the average absolute error across all samples, 
    RMSE is the square root of the average squared error, 
    and R2 is the coefficient of determination indicating how well the predictions fit the actual data.
    Percent error is computed as MAPE over non-zero ground-truth samples."""
    
    model.eval()
    results = []
    y_true = []
    y_pred = []
    if not silent:
        print(f"\n{'Sample ID':<20} | {'Actual':<8} | {'Pred':<8} | {'Abs Err':<8}")
        print("-" * 65)

    total_loss = 0.0
    criterion = nn.MSELoss()

    with torch.no_grad():
        for images, labels, filenames in loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            total_loss += loss.item()
            
            out = outputs.item()
            act = labels.item()
            err = abs(out - act)

            y_pred.append(out)
            y_true.append(act)
            results.append({'err': err})
            if not silent:
                print(f"{filenames[0]:<20} | {act:<8.2f} | {out:<8.2f} | {err:<8.2f}")

    mae = np.mean([r['err'] for r in results])
    rmse = np.sqrt(np.mean([(t - p) ** 2 for t, p in zip(y_true, y_pred)]))
    avg_loss = total_loss / len(loader)

    y_true_arr = np.array(y_true)
    y_pred_arr = np.array(y_pred)
    ss_res = np.sum((y_true_arr - y_pred_arr) ** 2)
    ss_tot = np.sum((y_true_arr - np.mean(y_true_arr)) ** 2)
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else float('nan')


    #percentage error is computed only on non-zero targets to avoid divide-by-zero on blank samples
    non_zero_mask = np.abs(y_true_arr) > 1e-8
    pct_error = (
        np.mean(np.abs((y_true_arr[non_zero_mask] - y_pred_arr[non_zero_mask]) / y_true_arr[non_zero_mask])) * 100
        if np.any(non_zero_mask)
        else float('nan')
    )

    if not silent:
        print("-" * 65)
        print(f"PERFORMANCE: MAE: {mae:.2f} | RMSE: {rmse:.2f} | R2: {r2:.4f} | %Err: {pct_error:.2f}%")
        print("-" * 65)
    
    return avg_loss, mae, rmse, r2, pct_error

def train_model(data_dir):
    """Trains the ResNet model on the plant counting dataset with early stopping based on validation loss.
    The pipeline includes data augmentation, dataset preparation, model training, and final evaluation on the test set using the best saved model.
    The model is a customization of ResNet18 with the final fully connected layer modified for regression output.
    Early stopping is implemented to halt training if the validation loss does not improve for a specified number of epochs.
    The training process includes periodic logging of training and validation loss, as well as the number of epochs without improvement."""
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    num_epochs = 100
    batch_size = 8
    patience = 15  # STOP training if val_loss doesn't improve for 15 epochs
    epochs_no_improve = 0
    
    transform = build_resnet_transform()

    print(f"[Train] Starting train_model with data_dir={data_dir}")
    print("[Train] Generating augmented images...")

    os.makedirs(MODEL_OUTPUT_DIR, exist_ok=True)

    batch_augment(
        input_dir=data_dir,
        output_dir=os.path.join(data_dir, "augmented"),
        multiplier=5,
    )
    print("[Train] Augmentation complete.")

    csv_path = os.path.join(data_dir, "metadata.csv")
    unique_ids = [str(x).strip() for x in pd.read_csv(csv_path)['file_name'].unique().tolist()]
    print(f"[Split] unique_base_ids={len(unique_ids)}")
    
    # We add 'blank_train' to the training ID pool so the blanks stay in training
    train_val_ids, test_ids = train_test_split(unique_ids, test_size=0.2, random_state=0)
    train_ids, val_ids = train_test_split(train_val_ids, test_size=0.125, random_state=0)
    print(f"[Split] train_base={len(train_ids)}, val_base={len(val_ids)}, test_base={len(test_ids)}")
    
    # Add the special blank base_id specifically to train_ids
    #The blank_train id is injected after splitting so the hard-negative sample never leaks into validation or test sets
    train_ids = np.append(train_ids, 'blank_train')

    full_dataset = PlantCountDataset(
        csv_path,
        data_dir,
        transform=transform,
    )

    train_idx = [i for i, s in enumerate(full_dataset.samples) if s['base_id'] in train_ids]
    val_idx = [i for i, s in enumerate(full_dataset.samples) if s['base_id'] in val_ids]
    test_idx = [i for i, s in enumerate(full_dataset.samples) if s['base_id'] in test_ids]
    print(f"[Index] train_samples={len(train_idx)}, val_samples={len(val_idx)}, test_samples={len(test_idx)}")

    train_aug = sum(1 for i in train_idx if "_aug_" in full_dataset.samples[i]['id'])
    val_aug = sum(1 for i in val_idx if "_aug_" in full_dataset.samples[i]['id'])
    test_aug = sum(1 for i in test_idx if "_aug_" in full_dataset.samples[i]['id'])
    print(f"[Index] train_aug={train_aug}, val_aug={val_aug}, test_aug={test_aug}")
    
    train_loader = DataLoader(Subset(full_dataset, train_idx), batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(Subset(full_dataset, val_idx), batch_size=1, shuffle=False)
    test_loader = DataLoader(Subset(full_dataset, test_idx), batch_size=1, shuffle=False)
    print(f"[Loader] train_batches={len(train_loader)}, val_batches={len(val_loader)}, test_batches={len(test_loader)}")

    model = models.resnet18(weights=RESNET18_WEIGHTS)
    model.fc = nn.Linear(model.fc.in_features, 1)
    model.to(device)
    
    optimizer = optim.Adam(model.parameters(), lr=0.0008)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=40, gamma=0.5)
    criterion = nn.MSELoss()

    best_val_loss = float('inf')

    print(f"--- Training on {device} with Early Stopping ---")
    for epoch in range(num_epochs):
        model.train()
        train_loss = 0.0
        for images, labels, _ in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            loss = criterion(model(images), labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
        
        val_loss, _, _, _, _ = evaluate_model(model, val_loader, device, silent=True)
        scheduler.step()

        # Check for improvement
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), MODEL_WEIGHTS_PATH)
            epochs_no_improve = 0
        else:
            epochs_no_improve += 1

        if (epoch + 1) % 5 == 0:
            avg_train = train_loss / len(train_loader)
            print(f"Epoch [{epoch+1}/{num_epochs}] | Train Loss: {avg_train:.2f} | Val Loss: {val_loss:.2f} | No Improve: {epochs_no_improve}")

        # EARLY STOPPING TRIGGER
        if epochs_no_improve >= patience:
            print(f"!!! EARLY STOPPING at epoch {epoch+1} !!!")
            break

    print("\n--- Final Test on Best Saved Model ---")
    model.load_state_dict(torch.load(MODEL_WEIGHTS_PATH))
    evaluate_model(model, test_loader, device)

def predict_carrot_count(image_path, model_weights_path=MODEL_WEIGHTS_PATH):
    """Loads the trained model and predicts the carrot count for a single image."""
    # 1. Setup Device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 2. Re-initialize Model Architecture
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, 1)
    
    # 3. Load Saved Weights
    if not os.path.exists(model_weights_path):
        raise FileNotFoundError(f"Weights file {model_weights_path} not found.")
        
    model.load_state_dict(torch.load(model_weights_path, map_location=device))
    model.to(device)
    model.eval()

    # 4. Define Inference Transforms
    # Must match the training normalization and size
    inference_transform = build_resnet_transform()

    # 5. Process Image
    try:
        image = Image.open(image_path).convert("RGB")
        input_tensor = inference_transform(image).unsqueeze(0) # Add batch dimension
        input_tensor = input_tensor.to(device)
    except Exception as e:
        return f"Error loading image: {e}"

    # 6. Run Inference
    with torch.no_grad():
        output = model(input_tensor)
        prediction = output.item()

    # 7. Post-processing
    final_count = max(0, prediction)
    
    return final_count

if __name__ == "__main__":
    train_model(data_dir="./data")
#    count = predict_carrot_count("data/2_3.jpg")
#    print (count)
