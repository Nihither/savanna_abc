from django.db import models
import uuid

from stuff.models import Profile


# Create your models here.
class Chat(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name="UUID")
    person1 = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name='chats_person1', editable=False,
                                verbose_name="Профиль 1")
    person2 = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name='chats_person2', editable=False,
                                verbose_name="Профиль 2")

    class Meta:
        unique_together = ('person1', 'person2')

    def __str__(self):
        return f"{self.person1} - {self.person2}"
