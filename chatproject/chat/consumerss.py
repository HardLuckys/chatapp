import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from users.models import CustomUser
from .models import ChatMessage, ChatRoom
from .message import message_cheker
from datetime import datetime
import base64
from django.core.files.base import ContentFile
from rest_framework.authtoken.models import Token

class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def save_message(self, message, image=None):
        chatroom = ChatRoom.objects.get(room_name=self.scope['url_route']['kwargs']['room_name'])
        mess = ChatMessage.objects.create(user=self.scope["user"], message=message, image=image, chatroom=chatroom)
        print('NEW MESSAGEEEEE ', mess)
        return mess

    @database_sync_to_async
    def messages_count(self):
        chatroom = ChatRoom.objects.get(room_name=self.scope['url_route']['kwargs']['room_name'])
        return ChatMessage.objects.filter(chatroom=chatroom).count()

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

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    # Receive message from WebSocket От тебя
    async def receive(self, text_data):
        #print('Receive message from WebSocket: ', message)
        text_data_json = json.loads(text_data)
        message = message_cheker(text_data_json['message'])
        if text_data_json['image'] != 'None':
            ext = text_data_json['image'].split(';base64,')[0]
            image = ContentFile(base64.b64decode(text_data_json['image'].split(",")[1]), name='temp.' + ext.split('/')[-1])
        else:
            image = None
        global mess
        mess = await self.save_message(message = message_cheker(text_data_json['message']), image=image)
        # Send message to room group
        if mess.image:
            img = mess.image.url
        else:
            img = 'None'
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': mess.user.username,
                'date': mess.date_send().__str__(),
                'avatar': mess.user.avatar.url,
                'image': img,
                'count': await self.messages_count()
            }
        )

    # Receive message from room group к тебе от
    async def chat_message(self, event):
        #print('Receive message from room group: ', message)
        message = event['message']
        if mess.image:
            img = mess.image.url
        else:
            img = 'None'
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': mess.user.username,
            'date': mess.date_send().__str__(),
            'avatar': mess.user.avatar.url,
            'image': img,
            'count': await self.messages_count()
        }))
