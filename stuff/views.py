from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date, time


# Index view
@login_required
def index(request):
    d = datetime.today()
    # students_coming_birthdays_this_week = Student.objects.filter(birthday__week=d.isocalendar().week)
    # teachers_coming_birthdays_this_week = Teacher.objects.filter(birthday__week=d.isocalendar().week)
    # students_coming_birthdays_next_week = Student.objects.filter(birthday__week=d.isocalendar().week + 1)
    # teachers_coming_birthdays_next_week = Teacher.objects.filter(birthday__week=d.isocalendar().week + 1)
    context = {
        # "students_coming_birthdays_this_week": students_coming_birthdays_this_week,
        # "students_coming_birthdays_next_week": students_coming_birthdays_next_week,
        # "teachers_coming_birthdays_this_week": teachers_coming_birthdays_this_week,
        # "teachers_coming_birthdays_next_week": teachers_coming_birthdays_next_week,
    }
    return render(request, 'stuff/index.html', context=context)
