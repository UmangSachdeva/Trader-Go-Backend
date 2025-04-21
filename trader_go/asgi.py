"""
ASGI config for trader_go project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from stock.consumers import ChatConsumer
# from channels.auth import AuthMiddlewareStack
from channels.auth import AuthMiddlewareStack
from .routing import websocket_urlpatterns
from channels.security.websocket import AllowedHostsOriginValidator

import trader_go.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trader_go.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
