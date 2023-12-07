from django.db import models
import uuid


# Create your models here.
class Chat(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name="UUID")
    manager = models.ForeignKey(to='stuff.Profile', on_delete=models.CASCADE, related_name='manager_chats',
                                blank=True, null=True, verbose_name="Менеджер")
    teacher = models.ForeignKey(to='stuff.Profile', on_delete=models.CASCADE, related_name='teacher_chats',
                                blank=True, null=True, verbose_name="Преподаватель")
    student = models.ForeignKey(to='stuff.Profile', on_delete=models.CASCADE, related_name='student_chat',
                                blank=True, null=True, verbose_name="Студент")

    class Meta:
        unique_together = ('manager', 'teacher', 'student')

    def __str__(self):
        return f"{self.uuid}"
