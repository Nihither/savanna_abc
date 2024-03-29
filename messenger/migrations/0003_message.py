# Generated by Django 4.1.7 on 2023-12-09 05:52

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stuff', '0003_alter_teacher_profile'),
        ('messenger', '0002_chat_name_chat_rmv'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=500, verbose_name='Сообщение')),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='Дата создания')),
                ('updated', models.BooleanField(default=False, verbose_name='Обновлено')),
                ('updated_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='Дата обновления')),
                ('rmv', models.BooleanField(default=False, verbose_name='Удалено')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='messenger.chat', verbose_name='Чат')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='stuff.profile', verbose_name='Отправитель')),
            ],
        ),
    ]
