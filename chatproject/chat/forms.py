from django import forms
from .models import ChatRoom

class ChatRoomCreateForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['room_name',]
