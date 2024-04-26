from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,JsonResponse
from django.views.generic import View
import os
from django.conf import settings
import socket
from django.core.cache import cache
from django.conf import settings

class SetupDownloadView(View):
    def get(self, request):

        if cache.get('sensor_status'):
            unique_token = request.GET.get('token')
        # Check if the provided token matches the one stored in the cache
            if unique_token != cache.get('unique_token'):
                return JsonResponse({'message': 'Invalid or expired token'}, status=400)
        	# hostname = socket.gethostname()
        	# # Get the IP address corresponding to the hostname
        	# ip_address = socket.gethostbyname(hostname)
            client_ip = request.META.get('REMOTE_ADDR')

            script_content = f"""#!/bin/bash
# Check if the user is root
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

# Define variables
HOST_NAME='{settings.SERVER_IP}'
HOST_PORT='{settings.SERVER_PORT}'
APP_TAR_URL="http://$HOST_NAME:$HOST_PORT/download/client/?token={cache.get('unique_token')}"
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

echo "ALLOWED_HOSTS = ['127.0.0.1','{client_ip}','$HOST_NAME']" >> $APP_DIR/client/settings.py

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
systemctl restart "$APP_NAME"

sleep 5
curl -d "token={cache.get('unique_token')}" -X POST http://$HOST_NAME:$HOST_PORT/client/sensor/


	"""

            response = HttpResponse(script_content, content_type='application/force-download')
        	# Set the content-disposition header to force a download
            response['Content-Disposition'] = 'attachment; filename="setup.sh"'
            return response
        return JsonResponse({'message': 'Please start the lissoner'}, status=503)

class ClientDownloadView(View):
    def get(self, request):
        if cache.get('sensor_status'):
            unique_token = request.GET.get('token')
            # Check if the provided token matches the one stored in the cache
            if unique_token != cache.get('unique_token'):
                return JsonResponse({'message': 'Invalid or expired token'}, status=400)
            # Path to the file you want to download
            file_path = os.path.join(settings.BASE_DIR, 'files', 'client.tar.gz')

            # Check if the file exists
            if os.path.exists(file_path):
                # Open the file in binary mode for reading
                with open(file_path, 'rb') as file:
                    # Create an HTTP response with the file as content
                    response = HttpResponse(file.read(), content_type='application/octet-stream')
                    # Set the content-disposition header to force a download
                    response['Content-Disposition'] = 'attachment; filename="client.tar.gz"'
                    return response
            else:
                # If the file does not exist, return a 404 Not Found response
                return HttpResponse('File not found', status=404)
        return JsonResponse({'message': 'Please start the lissoner'}, status=503)