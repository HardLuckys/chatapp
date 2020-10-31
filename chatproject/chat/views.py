from .models import ChatRoom, ChatMessage
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import ChatRoomSerializer, ChatMessageSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
import json

class Rooms(generics.ListAPIView):
    """
    Комнаты
    """
    serializer_class = ChatRoomSerializer
    def get_queryset(self):
        queryset = ChatRoom.objects.all()
        return queryset

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class Room(generics.ListAPIView):
    """
    Комната
    """
    pagination_class = StandardResultsSetPagination
    serializer_class = ChatMessageSerializer
    def get_queryset(self):
        try:
            room_name = self.kwargs['room_name']
            room = ChatRoom.objects.get(room_name=room_name)
            #messages = ChatMessage.objects.filter(chatroom=room)
            messages = room.chatroom.all()
        except:
            return Response({'error': "Not found"})
        return messages

    # def post(self, request, format=None):
    #     serializer = SnippetSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
