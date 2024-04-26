#!/bin/bash
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi
# Update the system
apt update

# Ask for server IP and port
read -p "Enter server IP: " server_ip
read -p "Enter server port: " server_port

# Set server folder path
server_folder="/usr/share"

# Clone server repository
cp -r server/ $server_folder

# Navigate to server folder
cd $server_folder/server

# Create .env file and write server IP and port
cat <<EOF > server/.env
SERVER_IP=$server_ip
SERVER_PORT=$server_port
EOF

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Deactivate virtual environment
deactivate

# Create a Systemd service file
cat <<EOF | sudo tee /etc/systemd/system/server.service
[Unit]
Description=Server For Docker

[Service]
User=root
Group=root
WorkingDirectory=$server_folder/server
Environment="PATH=$server_folder/server/venv/bin"
ExecStart=$server_folder/server/venv/bin/python $server_folder/server/manage.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload Systemd to detect the new service
sudo systemctl daemon-reload

# Enable and start the service
sudo systemctl enable server
sudo systemctl start server

echo "Setup complete. Server is now running."
