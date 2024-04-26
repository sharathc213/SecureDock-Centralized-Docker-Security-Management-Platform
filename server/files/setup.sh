#!/bin/bash
# Check if the user is root
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

# Define variables
HOST_NAME='localhost'
APP_TAR_URL="http://$HOST_NAME/client.tar.gz"
APP_NAME="client"
VENV_DIR="/usr/share/$APP_NAME/env"
APP_DIR="/usr/share/$APP_NAME"
ENV_FILE="/usr/share/$APP_NAME/.env"
# Download and extract the tar file
mkdir -p "$APP_DIR"
curl -L "$APP_TAR_URL" | tar -xz -C "$APP_DIR" --strip-components=1

# Create and activate virtual environment
python -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"


# Install required packages
pip install -r "$APP_DIR/requirements.txt"

# Define the path to the .env file


# Check if the .env file already exists, if not, create it
if [ ! -f "$ENV_FILE" ]; then
    touch "$ENV_FILE"
fi

# Write the environment variable assignments to the .env file
echo "HOSTNAME=$HOST_NAME" >> "$ENV_FILE"

chmod 600 "$ENV_FILE"

# Create systemd service unit file
cat <<EOF > "/etc/systemd/system/$APP_NAME.service"
[Unit]
Description=Client Application Fror Docker Security
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=$APP_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/python $APP_DIR/manage.py runserver 0.0.0.0:5234
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd daemon
systemctl daemon-reload

# Start and enable the systemd service
systemctl enable "$APP_NAME"
systemctl start "$APP_NAME"
