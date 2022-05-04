"""
ASGI config for djchanels project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from home.consumers import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djchanels.settings')

application = get_asgi_application()

ws_patterns = [

    path("ws/test/", TestConsumer.as_asgi()),
    path("ws/new/", NewConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    # "http": get_asgi_application(),
    'websocket': URLRouter(ws_patterns)
})
