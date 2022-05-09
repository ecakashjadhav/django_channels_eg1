from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer,JsonWebsocketConsumer

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
        self.accept()

    def receive_json(self, content, **kwargs):
        print('msg received..',content)
        self.send_json({"msg":"send from server to client"})

    def disconnect(self,close_code):
        print('Websocker disconnected',close_code)


class MyAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print('Websocker connected')
        await self.accept()

    async def receive_json(self, content, **kwargs):
        print('msg received..',content)
        await self.send_json({"msg":"send from server to client"})

    async def disconnect(self,close_code):
        print('Websocker disconnected',close_code)