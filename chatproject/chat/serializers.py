from rest_framework import serializers
from .models import ChatRoom, ChatMessage

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['room_name',]



class ChatMessageSerializer(serializers.ModelSerializer):
    chatroom = ChatRoomSerializer()
    class Meta:
        model = ChatMessage
        fields = '__all__'
