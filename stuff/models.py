from django.db import models
import uuid

from django.contrib.auth.models import User
from messenger.models import Chat


# Create your models here...
class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.SET_NULL, null=True, blank=True, related_name='profiles',
                                verbose_name="Аккаунт")
    first_name = models.CharField(verbose_name="Имя", max_length=50)
    last_name = models.CharField(verbose_name="Фамилия", max_length=30, blank=True, null=True)
    birthday = models.DateField(verbose_name="День рождения", blank=True, null=True)
    role = models.ForeignKey(to='Role', on_delete=models.SET_NULL, blank=True, null=True, related_name='profiles',
                             verbose_name="Роль")
    uuid = models.UUIDField(verbose_name="UUID", unique=True, default=uuid.uuid4, editable=False)
    rmv = models.BooleanField(verbose_name="Архивная запись", default=False)

    def full_name(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.first_name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Role(models.Model):
    code = models.CharField(verbose_name="Роль", max_length=10)

    def __str__(self):
        return self.code


class Contact(models.Model):
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE, related_name='contacts', verbose_name="Профиль")
    phone = models.CharField(verbose_name="Телефон", max_length=15, blank=True, null=True)
    email = models.EmailField(verbose_name="email", max_length=30, blank=True, null=True)
    additional_contact = models.CharField(verbose_name="Дополнительный контакт", max_length=30, blank=True, null=True)
    additional_contact_description = models.CharField(verbose_name="Описание", max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Контакт {self.profile.full_name()}"


class Teacher(models.Model):
    profile = models.OneToOneField(to=Profile, on_delete=models.CASCADE, related_name='teacher',
                                   verbose_name="Профиль")
    manager = models.ForeignKey(to=Profile, on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='managing_teachers', verbose_name="Менеджер")

    def __str__(self):
        return self.profile.full_name()

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Teacher, self).save(*args, **kwargs)
            # Add new chat teacher-manager
            new_chat = Chat()
            new_chat.participants.add(self.profile, self.manager)
            new_chat.save()
        else:
            super(Teacher, self).save(*args, **kwargs)


class Student(models.Model):
    profile = models.OneToOneField(to=Profile, on_delete=models.CASCADE, related_name='student', verbose_name="Профиль")
    is_adult = models.BooleanField(verbose_name="Взрослый", default=True)
    trustee = models.OneToOneField(to=Profile, on_delete=models.SET_NULL, related_name='child',  blank=True, null=True,
                                   verbose_name="Контактное лицо")
    manager = models.ForeignKey(to=Profile, on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='managing_students', verbose_name="Менеджер")

    def __str__(self):
        return self.profile.full_name()

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Student, self).save(*args, **kwargs)
            # Add new chat student-manager
            new_chat = Chat()
            new_chat.participants.add(self.profile, self.manager)
            new_chat.save()
        else:
            super(Student, self).save(*args, **kwargs)
