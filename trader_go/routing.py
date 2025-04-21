from django.urls import re_path

from stock import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/chat/(?P<room_name>\w+)/(?P<temperature>\w+)/$",
        consumers.ChatConsumer.as_asgi(),
    ),
]
