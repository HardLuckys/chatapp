from django.db import models
from django.conf import settings
from django.utils.translation import activate
from django.utils import formats
from django.shortcuts import reverse


class ChatRoom(models.Model):
    room_name = models.CharField(unique=True, max_length=100, verbose_name="ссылка")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, verbose_name="создатель")

    #chat_password = models.CharField(max_length=100, verbose_name="пароль")

    def get_absolute_url(self):
        return reverse('room', kwargs={'room_name':self.room_name})

    def __str__(self):
        return self.room_name

class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="пользователь")
    message = models.TextField(max_length = 500, verbose_name="сообщение")
    date = models.DateTimeField(auto_now_add=True, verbose_name="дата")
    image = models.ImageField(upload_to='chat', blank=True, verbose_name="картинка")
    chatroom = models.ForeignKey(ChatRoom, blank=True, related_name='chatroom', null=True, on_delete=models.CASCADE, verbose_name="комната")

    def date_send(self):
        activate('ru')
        date = formats.date_format(self.date, format="t N Y H:i")
        return date

    def __str__(self):
        return 'Сообщение: ' + self.message[:10] + '...' + ' От: ' + self.user.username

    class Meta:
        verbose_name = "Сообщения"
        verbose_name_plural = "Чат"
