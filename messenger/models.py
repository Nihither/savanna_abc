from django.db import models
import uuid


# Create your models here.
class Chat(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name="UUID")
    participants = models.ManyToManyField(to='stuff.Profile', related_name='chats')

    def __str__(self):
        return f"{self.uuid}"
