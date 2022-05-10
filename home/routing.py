from django.urls import path
from . import consumers

ws_patterns=[
    path("ws/test/", consumers.TestConsumer.as_asgi()),
    path("ws/new/", consumers.NewConsumer.as_asgi()),
    path("ws/jwc/<str:groupname>/", consumers.MyJsonWebsocketConsumer.as_asgi()),# chat sync
    path("ws/ajwc/<str:groupname>/", consumers.ChatAsyncJsonWebsocketConsumer.as_asgi()),# chat async
    path("ws/jawc/", consumers.MyAsyncJsonWebsocketConsumer.as_asgi()),
]