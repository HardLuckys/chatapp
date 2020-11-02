import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from users.models import CustomUser
from .models import ChatMessage, ChatRoom
from .message import message_cheker
from datetime import datetime
import base64
from django.core.files.base import ContentFile
from rest_framework.authtoken.models import Token
from django.utils import formats

class ChatConsumer(AsyncJsonWebsocketConsumer):

    @database_sync_to_async
    def save_message(self, message, image=None):
        chatroom = ChatRoom.objects.get(room_name=self.scope['url_route']['kwargs']['room_name'])
        mess = ChatMessage.objects.create(user=self.scope["user"], message=message, image=image, chatroom=chatroom)
        return mess

    @database_sync_to_async
    def is_creator(self):
        try:
            creator = ChatRoom.objects.get(creator=self.scope["user"], room_name=self.scope['url_route']['kwargs']['room_name'])
            return True
        except:
            return False


    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope["user"].username
        print('BoooooooooooT OH ', self.user)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_connect',
                'user': self.user,
            }
        )

    # Receive message from WebSocket От тебя
    async def receive_json(self, content):
        global mess
        mess = await self.save_message(message = content['message'])
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': content['message'],
                'user': mess.user.username,
                'date': formats.date_format(mess.date, format="t N Y H:i")
            }
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(json.dumps({
            'message': message,
            'user': mess.user.username,
            'date': formats.date_format(mess.date, format="t N Y H:i")
        }))

    async def user_connect(self, event):
        user = event['user']
        await self.send(json.dumps({
            'connected_user': user
        }))

    async def user_disconnect(self, event):
        user = event['user']
        await self.send(json.dumps({
            'disconnected_user': user
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_disconnect',
                'user': self.user,
            }
        )
