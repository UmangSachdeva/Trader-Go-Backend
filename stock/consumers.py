# consumers.py
import asyncio
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import websockets

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope)
        self.room_name = self.scope["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.external_socket_url = 'wss://ws.finnhub.io?token=cqp0g29r01qqj5dmh6pgcqp0g29r01qqj5dmh6q0'
        self.external_socket = await websockets.connect(self.external_socket_url)
        await self.accept()

    async def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        await self.external_socket.close()
        await self.close()

    async def receive(self, text_data):
        await self.external_socket.send(text_data)
        response = await self.external_socket.recv()

        await self.send(text_data=response)

    async def receive_json(self, content):
        await self.external_socket.send(json.dumps(content))
        response = await self.external_socket.recv()
        await self.send(json.loads(response))
