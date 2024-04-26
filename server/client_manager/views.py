from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.generic import View
import os
import json
from .models import Client
from django.core.cache import cache
import uuid
import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib import messages

channel_layer = get_channel_layer()




def check_client_online(client):
    try:

        # Send a GET request to the client's URL
        ip_address = client['ip_address']
        response = requests.get(f'http://{ip_address}:5234/')
      
        
        # Check if the response status code is OK (200)
        if response.status_code == 200:
            # Assuming the response is JSON, parse it and check the content
            json_response = response.json()
            if json_response.get('status') == 'online':
                return True  # Client is online
            else:
                return False  # Client is offline
        else:
            return False  
    except requests.RequestException:
        return False



class EnableSensor(View):
    def get(self, request):
        return JsonResponse({'message': 'GET method not allowed'}, status=405)
    def post(self, request):
        if request.user.is_authenticated:
            token=str(uuid.uuid4())
            cache.set('sensor_status', True,timeout=60)
            cache.set('unique_token', token,timeout=60)
            return JsonResponse({'message': True,'token':token,'ip':settings.SERVER_IP,'port':settings.SERVER_PORT})
        return JsonResponse({'message': 'User is not authenticated'}, status=401)

class DisableSensor(View):
    def get(self, request):
        return JsonResponse({'message': 'GET method not allowed'}, status=405)
    def post(self, request):
        if request.user.is_authenticated:
            cache.clear()
            return JsonResponse({'message': True})
        return JsonResponse({'message': 'User is not authenticated'}, status=401)


class CaptureClient(View):
    def get(self, request):
        if not cache.get('sensor_status'):
            return JsonResponse({'message': 'Please start the lissoner'}, status=503)
        return JsonResponse({'message': 'GET method not allowed'}, status=405)
    def post(self, request):
        if not cache.get('sensor_status'):
            return JsonResponse({'message': 'Please start the lissoner'}, status=503)
        unique_token = request.POST.get('token')
  
        # Check if the provided token matches the one stored in the cache
        if unique_token != cache.get('unique_token'):
            return JsonResponse({'message': 'Invalid or expired token'}, status=400)
        try:
            client_ip = request.META.get('REMOTE_ADDR')  # Get the client's IP address from the request
            url = f'http://{client_ip}:5234/token/'
            data = {
    'username': 'admin',
    'password': 'admin'
}

            try:
                response = requests.post(url, data=data)
                token = json.loads(response.text).get('token')
            except Exception as e:
            # Handle any errors that occur during the request
                return JsonResponse({'message': str(e)}, status=500)

            if client_ip and token:
                    # Check if the IP address already exists in the database
                if Client.objects.filter(ip_address=client_ip).exists():
                    client = Client.objects.get(ip_address=client_ip)
                    client.token = token  # Generate a new token
                    client.save()
                    data={'data':'info','message':'Token Update Successfull','ip':client_ip}
                    async_to_sync(channel_layer.group_send)(
            "output",  # Replace with a unique group name
            {
                "type": "send_output",
                "text": json.dumps(data)
            }
        )
                    return JsonResponse({'message': True})
                else:
                        # Save the IP address to the database
                    Client.objects.create(ip_address=client_ip, token=token)
                    cache.clear()
                    data={'data':'data','ip':client_ip}
                    async_to_sync(channel_layer.group_send)(
            "output",  # Replace with a unique group name
            {
                "type": "send_output",
                "text": json.dumps(data)
            }
        )
                    return JsonResponse({'message': True,})
            else:
                return JsonResponse({'message': 'Unable to capture IP address'}, status=400)
        except Exception as e:
                # Handle any other exceptions
            return JsonResponse({'message': str(e)}, status=500)
 


class ListClient(View):
    def get(self, request):
        return JsonResponse({'message': 'GET method not allowed'}, status=405)
    def post(self, request):
        if request.user.is_authenticated:
            try:
                        # Query all clients from the database
                clients = Client.objects.all().values('id', 'ip_address')

                # Convert queryset to list of dictionaries
                client_list = list(clients)
                for client in client_list:
                    is_online = check_client_online(client)
                    if is_online:
                        client['status'] = 'online'
                    else:
                        client['status'] = 'offline'
                # Return clients as JSON response
                return JsonResponse({'clients': client_list})
              
            except Exception as e:
                    # Handle any other exceptions
                return JsonResponse({'message': str(e)}, status=500)
 

class DeleteClient(View):
    def get(self, request):
        return JsonResponse({'message': 'GET method not allowed'}, status=405)
    def post(self, request):
        if request.user.is_authenticated:
            client_id = request.POST.get('id')
            try:
                        # Query all clients from the database
                client = Client.objects.get(id=client_id)
                client.delete()
                return JsonResponse({'message': 'Client deleted successfully'})
              
            except Exception as e:
                    # Handle any other exceptions
                return JsonResponse({'message': str(e)}, status=500)


class CountClient(View):
    def get(self, request):
        return JsonResponse({'message': 'GET method not allowed'}, status=405)
    def post(self, request):
        if request.user.is_authenticated:
            try:
                        # Query all clients from the database
                total_client = 0
                online_client = 0
                offline_client = 0 
             
                clients = Client.objects.all().values('id', 'ip_address')

                # Convert queryset to list of dictionaries
                client_list = list(clients)
                for client in client_list:
                    total_client = total_client + 1
                    is_online = check_client_online(client)
                    if is_online:
                        online_client = online_client + 1
                    else:
                        offline_client =offline_client + 1
           
                data = {
            'total_client': total_client,
            'online_client': online_client,
            'offline_client': offline_client
        }

   
                return JsonResponse(data)
              
            except Exception as e:
                    # Handle any other exceptions
                return JsonResponse({'message': str(e)}, status=500)
