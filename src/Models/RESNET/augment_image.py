import albumentations as A
import cv2
import os
from pathlib import Path

def batch_augment(input_dir, output_dir, multiplier=3):
    """
    input_dir: Path to original images
    output_dir: Where to save augmented images
    multiplier: How many augmented versions to create per original image
    """
    # Define the pipeline
    transform = A.Compose([
        A.HorizontalFlip(p=0.5),
        A.RandomBrightnessContrast(p=0.2),
        A.RGBShift(r_shift_limit=15, g_shift_limit=15, b_shift_limit=15, p=0.5),
        A.AdditiveNoise(noise_type="uniform", spatial_mode="constant", noise_params={"ranges": [(-0.2, 0.2), (-0.1, 0.1), (-0.1, 0.1)]}),
    ])

    # Create output path
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Supported extensions
    valid_extensions = ('.jpg', '.jpeg')

    # Loop through files
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(valid_extensions):
            img_path = os.path.join(input_dir, filename)
            image = cv2.imread(img_path)
            
            if image is None:
                print(f"Skipping {filename} (could not read)")
                continue
                
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            base_name = Path(filename).stem

            for i in range(multiplier):
                augmented = transform(image=image)['image']
                
                # Format: originalname_aug_0.jpg
                save_name = f"{base_name}_aug_{i}.jpg"
                save_path = os.path.join(output_dir, save_name)
                
                # Save back as BGR
                cv2.imwrite(save_path, cv2.cvtColor(augmented, cv2.COLOR_RGB2BGR))
            
            # print(f"Processed: {filename} -> {multiplier} variants")

if __name__ == "__main__":
    batch_augment("data", "data/augmented/", multiplier=5)