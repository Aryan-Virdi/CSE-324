def resnet_load(checkpoint_path, device):
    """Load the ResNet model and weights. Imports are deferred to reduce module import time."""
    import torch
    import torch.nn as nn
    from torchvision import models

    # 1. Replicate the architecture from your training script
    model = models.resnet18()
    # Match the final layer: model.fc = nn.Linear(512, 1)
    model.fc = nn.Linear(model.fc.in_features, 1)

    # 2. Load the state dict
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model.to(device)
    model.eval()
    return model


def resnet_count(image, model, device):
    """Run inference to estimate carrot counts. Imports are deferred to reduce module import time."""
    import torch
    from torchvision import transforms

    # 3. Match your training transformations
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    image_tensor = transform(image).unsqueeze(0).to(device) # Add batch dimension

    # 4. Run Inference
    with torch.no_grad():
        output = model(image_tensor)

    # Since it's regression, the output is the raw predicted count
    count = output.item()
    return max(0, count) # Counts shouldn't be negative

# Usage 

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model = resnet_load("src/Models/RESNET/model_weights.pth", device)
# image = Image.open("tests/representative_data/test_image_1.jpg").convert("RGB")
# predicted_value = resnet_count(image, model, device)

# print(f"Predicted Plant Count: {predicted_value:.2f}") 