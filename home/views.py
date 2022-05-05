from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import time
from django.http import JsonResponse
from .thread import *

# def home(request):
#     for i in range(0,10):
#         data = {'count':i}
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             'test_consumer_group', {
#                 'type':'send_notification',
#                 'value':json.dumps(data)
#             }
#         ) 
#         time.sleep(1)
#     return render(request,'home.html')


async def home(request):
    for i in range(1,10):
        data = {'count':i}
        channel_layer = get_channel_layer()
        await(channel_layer.group_send)(
            'new_consumer_group', {
                'type':'send_notification',
                'value':json.dumps(data)
            }
        ) 
        time.sleep(1)
    return render(request,'home.html')


def generate_student_data(request):
    total = request.GET.get('total')
    CreateStudentThread(int(total)).start()
    return JsonResponse({"status":200})

