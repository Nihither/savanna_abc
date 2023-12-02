from django.db import models
import uuid


# Create your models here.
class Chat(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name="UUID")
    first_person = models.ForeignKey(to='stuff.Profile', on_delete=models.CASCADE, related_name='chats_first_person',
                                     editable=False, verbose_name="Профиль 1")
    second_person = models.ForeignKey(to='stuff.Profile', on_delete=models.CASCADE, related_name='chats_second_person',
                                      editable=False, verbose_name="Профиль 2")

    class Meta:
        unique_together = ('first_person', 'second_person')

    def __str__(self):
        return f"{self.first_person} - {self.second_person}"
