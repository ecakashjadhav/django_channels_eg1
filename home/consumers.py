from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer,JsonWebsocketConsumer
from .models import *
from channels.db import database_sync_to_async

class TestConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name="test_consumer"
        self.room_group_name="test_consumer_group"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,self.channel_name
        )
        self.accept()
        self.send(text_data=json.dumps({'status':'connected'}))

    def receive(self,*, text_data):
        print(text_data)
        self.send(text_data=json.dumps({'status':'We got you'}))

    def disconnect(self,message):
        print("disconnect")

    def send_notification(self,event):
        print(event)
        data = json.loads(event.get('value'))
        self.send(text_data=json.dumps({'payload': data}))


class NewConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.room_name="new_consumer"
        self.room_group_name="new_consumer_group"
        await(self.channel_layer.group_add)(
            self.room_group_name,self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({'status':'new consumer connected'}))

    async def receive(self,*, text_data):
        # print(text_data)
        await self.send(text_data=json.dumps({'status':'We got you'}))

    async def disconnect(self,message):
        print("disconnect")

    async def send_notification(self,event):
        # print(event)
        data = json.loads(event.get('value'))
        await self.send(text_data=json.dumps({'payload': data}))

# chat app.
class MyJsonWebsocketConsumer(JsonWebsocketConsumer):
    def connect(self):
        print('Websocker connected')
        print("Channel Layer: ",self.channel_layer)
        print("Channel Name: ",self.channel_name)
        #get group name from url parameter
        self.group_name = self.scope['url_route']['kwargs']['groupname']
        print("Group Name: ",self.group_name)
        async_to_sync(self.channel_layer.group_add)(self.group_name,self.channel_name)
        self.accept()

    def receive_json(self, content, **kwargs):
        print('msg received..',content)
        group = Group.objects.get(name=self.group_name)
        chat = Chat(content = content['msg'],group=group)
        chat.save()
        async_to_sync(self.channel_layer.group_send)(self.group_name,{'type':'chat.message','message':content['msg']})
    
    def chat_message(self,event):
        print("Event: ",event)
        self.send_json({'message':event['message']})

    def disconnect(self,close_code):
        print('Websocker disconnected',close_code)
        async_to_sync(self.channel_layer.group_discard)(self.group_name,self.channel_name)


class MyAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print('Websocker connected')
        await self.accept()

    async def receive_json(self, content, **kwargs):
        print('msg received..',content)
        await self.send_json({"msg":"send from server to client"})

    async def disconnect(self,close_code):
        print('Websocker disconnected',close_code)


class ChatAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print('Websocker connected')
        print("Channel Layer: ",self.channel_layer)
        print("Channel Name: ",self.channel_name)
        #get group name from url parameter
        self.group_name = self.scope['url_route']['kwargs']['groupname']
        print("Group Name: ",self.group_name)
        await self.channel_layer.group_add(self.group_name,self.channel_name)
        await self.accept()

    async def receive_json(self, content, **kwargs):
        print('msg received..',content)
        group = await database_sync_to_async(Group.objects.get)(name=self.group_name)
        chat = Chat(content = content['msg'],group=group)
        await database_sync_to_async(chat.save)()
        await self.channel_layer.group_send(self.group_name,{'type':'chat.message','message':content['msg']})
    
    async def chat_message(self,event):
        print("Event: ",event)
        await self.send_json({'message':event['message']})

    async def disconnect(self,close_code):
        print('Websocker disconnected',close_code) 
        await self.channel_layer.group_discard(self.group_name,self.channel_name)