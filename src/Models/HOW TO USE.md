# Model Training and Evaluation
This is all information pertinent to training and evaluating the computer vision models.

# Training
Our dataset lives in Box, and the data are proprietary. Here's how you can live download the dataset from Box when training: 

## Manually configuring rclone
on your local machine:
    installed rclone: 
        sudo -v ; curl https://rclone.org/install.sh | sudo bash
    got rclone box credential: 
        rclone authorize "box" 
        (opens we browser) -> grant rclone access to box
        (terminal output) -> copy the entire output between the curly brackets (includes access_token, refresh_token, etc)

on the docker instance:
    installed unzip: 
        sudo apt-get update && sudo apt-get install -y unzip
    installed rclone: 
        sudo -v ; curl https://rclone.org/install.sh | sudo bash
    configured rclone:
        rclone config
            n
            remote
            box
            (enter)
            (enter)
            (enter)
            (enter)
            1
            n
            n
            (paste output from prior segment)
            y
    tested that rclone worked properly:
        rclone lsd remote:
        (this should list out your box home directory)
    copied calibration images from capstone folder directory:
        rclone copy remote:CSE\ 120\ Group\ 324/Field\ Data/Calibration\ Images ./data/Calibration_Images

## Using the Premade Scripts to copy the dataset
run the setup command: 
    bash src/Models/setup-rclone.sh
run the manual token setup:
    rclone config reconnect box:
    y
    n
    (generate new access token on your machine: rclone authorize "box" )
    (paste a new access token into the docker terminal)
run the download command:
    bash src/Models/copy-dataset.sh

## Manually Verifying the Dataset Loader Works
download torch and torchvision with pip:
    pip install torch torchvision
run the training.py file. expected output:
    number of labeled images: 30
    total carrots in row 1: 71.0
    image dimensions: (4624, 3472)

## Preprocessing and Data Augmentation Pipeline
Instead of training on the raw dataset data, we preprocess the images with a handful of scripts to boost training. 

run the segmentation.py file (dataset is loaded into codespace). expected output:
    Created 30 segmented images of shape (480, 480, 3)
    there should be 30 segmented images in data/Output
run the save-new-dataset.sh file.
    bash src/Models/save-new-dataset.sh
    go into box and rename the new Output folder to something more descriptive (so that it doesn't mix with future outputs.)
