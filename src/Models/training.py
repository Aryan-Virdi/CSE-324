import pandas as pd
import torch
from torch.utils.data import Dataset
from PIL import Image

class ImageRegressionDataset(Dataset):
    def __init__(self, directory):
        """
        Args:
            directory (string): Path to the images and metadata.csv. Assumes that they both live in the same folder
        """
        self.metadata = pd.read_csv(f"{directory}/metadata.csv")
        """ metadata columns:
        0 file_name
        1 field_ID
        2 image_number
        3 left_count
        4 right_count
        5 whole_count
        6 latitude
        7 longitude
        8 timestamp
        9 square feet
        """

    def __len__(self):
        return len(self.metadata)

    def __getitem__(self, idx):
        img_name = f"data/dataset/{self.metadata.iloc[idx, 0]}.jpg" # file names are stored in the first column of the metadata
        image = Image.open(img_name).convert('RGB')

        labels = self.metadata.iloc[idx]["whole_count"].astype('float32') # for now, we regress on the whole-image count
        labels = torch.tensor(labels) # the values must be floats due to pytorch regression models requiring float inputs

        return image, labels

if __name__ == "__main__":
    dataset = ImageRegressionDataset("./data/dataset")
    print(f"number of labeled images: {len(dataset)}")
    img, metadata = dataset.__getitem__(1)
    print(f"total carrots in row 1: {metadata}")
    print(f"image 1 dimensions: {img.size}")