from django.db import models
import uuid


# Create your models here.
class Chat(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name="UUID")
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Название чата")
    participants = models.ManyToManyField(to='stuff.Profile', related_name='chats')
    rmv = models.BooleanField(verbose_name="В архиве", default=False)

    def __str__(self):
        return f"{self.uuid}"
