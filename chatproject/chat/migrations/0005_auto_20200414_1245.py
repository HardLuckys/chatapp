# Generated by Django 2.2.2 on 2020-04-14 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20200414_1225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatroom',
            name='chatmessage',
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='chatroom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chatroom', to='chat.ChatRoom', verbose_name='комната'),
        ),
    ]
