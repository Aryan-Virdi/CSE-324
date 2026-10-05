# Sets up rclone for automatically pulling the dataset into the codespace from Box
mkdir -p ~/.config/rclone
cat << EOF > ~/.config/rclone/rclone.conf
[box]
type = box
token = $RCLONE_CONFIG_MYBOX_TOKEN
root_folder_id = 364615969403
EOF
# Note: this token may expire, so see the manual setup instructions for how to make a new token
sudo apt-get update && sudo apt-get install -y unzip
sudo -v ; curl https://rclone.org/install.sh | sudo bash
mkdir data/Output