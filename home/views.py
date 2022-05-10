from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import time
from django.http import HttpResponse, JsonResponse
from .thread import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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

def chat(request,group_name=None):
    print(group_name)
    g,created=Group.objects.get_or_create(name=group_name)
    chats = []
    if g:
        chats = Chat.objects.filter(group=g)
    return render(request,'chat.html',{"groupname":group_name,"chats":chats})


def generate_student_data(request):
    total = request.GET.get('total')
    CreateStudentThread(int(total)).start()
    return JsonResponse({"status":200})

def msgFromOutsider(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('india',{'type':'chat.message',
                                        'message':'Message from outside consumer'})
    return HttpResponse('Message sent from view to consumer')
