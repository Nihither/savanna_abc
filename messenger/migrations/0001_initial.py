# Generated by Django 4.1.7 on 2023-12-02 07:15

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stuff', '0002_student_manager_teacher_manager'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('first_person', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='chats_first_person', to='stuff.profile', verbose_name='Профиль 1')),
                ('second_person', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='chats_second_person', to='stuff.profile', verbose_name='Профиль 2')),
            ],
            options={
                'unique_together': {('first_person', 'second_person')},
            },
        ),
    ]
