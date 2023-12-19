import uuid
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from messenger.models import Chat
from .utils import get_days_array


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
    profile = models.OneToOneField(to=Profile, on_delete=models.CASCADE, related_name='contact',
                                   verbose_name="Профиль")
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
    rmv = models.BooleanField(verbose_name="Архивный", default=False)

    def __str__(self):
        return self.profile.full_name()

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Teacher, self).save(*args, **kwargs)
            # Add new chat teacher-manager
            new_chat = Chat()
            new_chat.save()
            new_chat.participants.add(self.profile, self.manager)
        else:
            super(Teacher, self).save(*args, **kwargs)


class Student(models.Model):
    profile = models.OneToOneField(to=Profile, on_delete=models.CASCADE, related_name='student', verbose_name="Профиль")
    is_adult = models.BooleanField(verbose_name="Взрослый", default=True)
    trustee = models.OneToOneField(to=Profile, on_delete=models.SET_NULL, related_name='child',  blank=True, null=True,
                                   verbose_name="Контактное лицо")
    manager = models.ForeignKey(to=Profile, on_delete=models.SET_NULL, blank=True, null=True,
                                related_name='managing_students', verbose_name="Менеджер")
    rmv = models.BooleanField(verbose_name="Архивный", default=False)

    def __str__(self):
        return self.profile.full_name()

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Student, self).save(*args, **kwargs)
            # Add new chat student-manager
            new_chat = Chat()
            new_chat.save()
            new_chat.participants.add(self.profile, self.manager)
        else:
            super(Student, self).save(*args, **kwargs)


class Class(models.Model):
    week_days = (
        (0, 'ПН'),
        (1, 'ВТ'),
        (2, 'СР'),
        (3, 'ЧТ'),
        (4, 'ПТ'),
        (5, 'СБ'),
        (6, 'ВС')
    )
    teacher = models.ForeignKey(to=Teacher, on_delete=models.SET_NULL, related_name='classes', blank=True, null=True,
                                verbose_name="Преподаватель")
    student = models.ForeignKey(to=Student, on_delete=models.SET_NULL, related_name='classes', blank=True, null=True,
                                verbose_name="Студент")
    day = models.SmallIntegerField(choices=week_days, verbose_name="День недели")
    start_time = models.TimeField(verbose_name="Время начала")
    duration = models.DurationField(verbose_name="Продолжительность", default=timedelta(hours=1))

    class Meta:
        unique_together = ['teacher', 'student', 'day', 'start_time']

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Class, self).save(*args, **kwargs)
            # add lessons for this class
            days_array = get_days_array(self.day)
            for date in days_array:
                new_lesson = Lesson(class_item=self, teacher=self.teacher, student=self.student, date=date,
                                    start_time=self.start_time)
                new_lesson.save()
        else:
            super(Class, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.teacher} {self.student} {self.day}"


class Lesson(models.Model):
    class_item = models.ForeignKey(to=Class, on_delete=models.CASCADE, related_name='lessons', blank=True, null=True,
                                   verbose_name="Окно")
    teacher = models.ForeignKey(to=Teacher, on_delete=models.SET_NULL, related_name='lessons', blank=True, null=True,
                                verbose_name="Преподаватель")
    student = models.ForeignKey(to=Student, on_delete=models.SET_NULL, related_name='lessons', blank=True, null=True,
                                verbose_name="Студент")
    date = models.DateField(verbose_name="Дата")
    start_time = models.TimeField(verbose_name="Время начала")
    duration = models.DurationField(verbose_name="Продолжительность", default=timedelta(hours=1))
    is_cancelled = models.BooleanField(default=False, verbose_name="Отменен")
    is_complete = models.BooleanField(default=False, verbose_name="Проведен")
    is_moved = models.BooleanField(default=False, verbose_name="Перенесен")
    moved_to = models.OneToOneField(to='self', on_delete=models.SET_NULL, blank=True, null=True,
                                    verbose_name="Перенесено на дату")

    class Meta:
        unique_together = ['teacher', 'student', 'date', 'start_time']

    def __str__(self):
        return f"{self.teacher} {self.student} {self.date} {self.start_time}"
