from savanna.local_settings import ENV
from django.http import HttpResponse
from .models import Profile
from savanna import secrets
from datetime import datetime, timedelta
import requests


def birthday_notification(request):
    bot_token = secrets.bot_token
    chat_id = secrets.chat_id[ENV]
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    date_today = datetime.today()
    text = ''
    for i in (1, 2):
        delta = timedelta(days=i)
        d = date_today + delta
        students = Profile.objects.filter(role__code='student', birthday__month=d.month) & \
            Profile.objects.filter(role__code='student', birthday__day=d.day)
        if students:
            text = text + f'Дни рождения учеников {d.day} {d.strftime("%b")} \n\n'
            for student in students:
                text = text + f"{student.first_name} {student.last_name}\n"
        teachers = Profile.objects.filter(role__code__in=['teacher', 'manager'], birthday__month=d.month) & \
            Profile.objects.filter(role__code__in=['teacher', 'manager'], birthday__day=d.day)
        if teachers:
            text = text + f'Дни рождения сотрудников {d.day} {d.strftime("%b")} \n\n'
            for teacher in teachers:
                text = text + f"{teacher.first_name} {teacher.last_name}\n"

    params = {
        'chat_id': chat_id,
        'text': text
    }
    if text:
        r = requests.post(url=url, params=params)

    return HttpResponse(request, r.status_code)
