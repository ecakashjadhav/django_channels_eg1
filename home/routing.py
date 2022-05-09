from django.urls import path
from . import consumers

ws_patterns=[
    path("ws/test/", consumers.TestConsumer.as_asgi()),
    path("ws/new/", consumers.NewConsumer.as_asgi()),
    path("ws/jwc/", consumers.MyJsonWebsocketConsumer.as_asgi()),
    path("ws/jawc/", consumers.MyAsyncJsonWebsocketConsumer.as_asgi()),
]