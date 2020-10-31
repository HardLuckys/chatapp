from django.shortcuts import render, redirect
from .models import ChatMessage, ChatRoom
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from .forms import ChatRoomCreateForm
import requests

def room(request, room_name):
    try:
        room = ChatRoom.objects.get(room_name=room_name)
        messages = ChatMessage.objects.filter(chatroom=room)
        return render(request, 'chat/room.html', {'room_name': room_name, 'messages': messages})
    except ObjectDoesNotExist:
        return redirect(index)

def index(request):
    url ='http://127.0.0.1:8000/chat/my-room/'
    r = requests.get(url)
    print(r.text)
    form = ChatRoomCreateForm()
    rooms = ChatRoom.objects.all()
    if request.method == 'GET':
        context = {
            'rooms': rooms,
            'form': form,
        }
        return render(request, 'chat/rooms_create.html', context)
    elif request.method == 'POST':
        bound_form = ChatRoomCreateForm(request.POST)
        if bound_form.is_valid():
            bound_form.instance.creator = request.user
            new_room = bound_form.save()
            return redirect(new_room.get_absolute_url())
        return render(request, 'chat/rooms_create.html', context={'rooms': rooms, 'form': bound_form})

def home(request):
    return render(request, 'home.html')
