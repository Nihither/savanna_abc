# Generated by Django 4.1.7 on 2023-12-01 19:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Фамилия')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='День рождения')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='UUID')),
                ('rmv', models.BooleanField(default=False, verbose_name='Архивная запись')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, verbose_name='Роль')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teachers', to='stuff.profile', verbose_name='Профиль')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_adult', models.BooleanField(default=True, verbose_name='Взрослый')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='stuff.profile', verbose_name='Профиль')),
                ('trustee', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child', to='stuff.profile', verbose_name='Контактное лицо')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profiles', to='stuff.role', verbose_name='Роль'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profiles', to=settings.AUTH_USER_MODEL, verbose_name='Аккаунт'),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Телефон')),
                ('email', models.EmailField(blank=True, max_length=30, null=True, verbose_name='email')),
                ('additional_contact', models.CharField(blank=True, max_length=30, null=True, verbose_name='Дополнительный контакт')),
                ('additional_contact_description', models.CharField(blank=True, max_length=100, null=True, verbose_name='Описание')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='stuff.profile', verbose_name='Профиль')),
            ],
        ),
    ]