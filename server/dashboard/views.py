from django.shortcuts import render
from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import json
import socket
import requests
from client_manager.models import Client
class Index(LoginRequiredMixin, View):
    def get(self, request):
        return render(request,"dashboard.html")


class CheckButtonStatus(View):
    def get(self, request):
        return JsonResponse({'message': 'GET method not allowed'}, status=405)

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'User is not authenticated'}, status=401)
        
        sensor_status = cache.get('sensor_status')
        if sensor_status == None:
            sensor_status=False
        return JsonResponse({'status': not sensor_status})




# class ScanView(LoginRequiredMixin, View):
#     def get(self, request):
#         return render(request,"scan.html")


class ScanView(LoginRequiredMixin, View):
    def post(self, request):
        # GET method is not allowed
        return JsonResponse({'message': 'GET method not allowed'}, status=405)
    
    def get(self, request):
        if request.user.is_authenticated:
            try:
                client_id = request.GET.get('id')  # Get client ID from the request
                # client_id = 22
                client = Client.objects.get(id=client_id)
    
                # Retrieve IP address and token
                client_ip = client.ip_address
                client_token = client.token
                         
                url = f'http://{client_ip}:5234/scan/'
                headers = {
                    'Authorization': f'Token {client_token}'
                }

                # Send the GET request
                response = requests.get(url, headers=headers)

                # Check the response status
                if response.status_code == 200:
                    # Request was successful
                    data = response.json()  # Extract data from response
                    # d = json.loads(data)
                    info_count = 0
                    pass_count = 0
                    warn_count = 0
                    note_count = 0
                    try:
                        # Load the JSON response
                        data = json.loads(data)
                        main_checks = []
                    

                        # Iterate over tests and their results
                        for test in data.get('tests', []):
                            main_id = test.get('id')
                            main_desc = test.get('desc')
                  
                            new = {'ID':main_id,'INFO': 0, 'PASS': 0, 'WARN': 0, 'NOTE': 0 ,'DESC':main_desc, 'RESULT':[]}
                            for result in test.get('results', []):
                         
                                new['RESULT'].append(result)
                                result_type = result.get('result')
                                new[result_type] += 1
                                if result_type == 'INFO':
                                    info_count += 1
                                elif result_type == 'PASS':
                                    pass_count += 1
                                elif result_type == 'WARN':
                                    warn_count += 1
                                elif result_type == 'NOTE':
                                    note_count += 1
                               
                            main_checks.append(new)
                        
                        total_checks = info_count + pass_count + warn_count + note_count
                        info_percentage = (info_count / total_checks) * 100 if total_checks > 0 else 0
                        pass_percentage = (pass_count / total_checks) * 100 if total_checks > 0 else 0
                        warn_percentage = (warn_count / total_checks) * 100 if total_checks > 0 else 0
                        note_percentage = (note_count / total_checks) * 100 if total_checks > 0 else 0
                        chart1={'TOTAL':total_checks,'WARN':round(warn_percentage,2),'INFO':round(info_percentage,2),'PASS':round(pass_percentage,2) ,'NOTE':round(note_percentage,2)}
                    
                    except json.JSONDecodeError as e:
                        messages.error(request, "Error decoding JSON:", e)
                        return HttpResponseRedirect(reverse('index'))
                      
                    except Exception as e:
                        messages.error(request, "Error occered:", e)
                        return HttpResponseRedirect(reverse('index'))
                    messages.success(request, "Scan successful") 
                    return render(request,"scan.html",{'chart1':chart1,'chart2':main_checks})
                elif response.status_code == 401 and response.json().get('detail') == 'Invalid token.':
#                     print("asdasdadsads")
#                     url = f'http://{client_ip}:5234/token/'
#                     data = {
#     'username': 'admin',
#     'password': 'admin'
# }

                    messages.error(request, "Invalid Token." )
                    return HttpResponseRedirect(reverse('index'))
                else:
                    messages.error(request, "Client Offline" )
                    return HttpResponseRedirect(reverse('index'))
 
            except Client.DoesNotExist:
                # Handle case where client with given ID does not exist
                messages.error(request, 'Client not found' )
                return HttpResponseRedirect(reverse('index'))
            except Exception as e:
                # Handle any other exceptions
                messages.error(request, "Client Offline" )
                return HttpResponseRedirect(reverse('index'))
        else:
            # User is not authenticated
            return JsonResponse({'message': 'User is not authenticated'}, status=401)


