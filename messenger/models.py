from django.db import models
from datetime import datetime
import uuid


# Create your models here.
class Chat(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name="UUID")
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Название чата")
    participants = models.ManyToManyField(to='stuff.Profile', related_name='chats')
    rmv = models.BooleanField(verbose_name="В архиве", default=False)

    def __str__(self):
        if self.name:
            return f"{self.name}"
        else:
            return f"{self.uuid}"


class Message(models.Model):
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE, related_name='messages',
                             verbose_name="Чат")
    sender = models.ForeignKey(to='stuff.Profile', on_delete=models.CASCADE, related_name='sent_messages',
                               verbose_name="Отправитель")
    body = models.CharField(max_length=500, verbose_name="Сообщение")
    created_date = models.DateTimeField(default=datetime.now, verbose_name="Дата создания")
    updated = models.BooleanField(default=False, verbose_name="Обновлено")
    updated_date = models.DateTimeField(default=datetime.now, verbose_name="Дата обновления")
    rmv = models.BooleanField(default=False, verbose_name="Удалено")

    def __str__(self):
        return f"{self.sender}"
