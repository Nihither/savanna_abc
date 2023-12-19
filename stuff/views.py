from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.utils.safestring import mark_safe
from datetime import date
from .models import Profile, Class, Lesson
from .calendar import Calendar


# Index view

@login_required
def index(request):
    d = date.today()
    students_coming_birthdays_this_week = \
        Profile.objects.filter(role__code='student', birthday__week=d.isocalendar().week)
    teachers_coming_birthdays_this_week = \
        Profile.objects.filter(role__code__in=['teacher', 'manager'], birthday__week=d.isocalendar().week)
    students_coming_birthdays_next_week = \
        Profile.objects.filter(role__code='student', birthday__week=d.isocalendar().week + 1)
    teachers_coming_birthdays_next_week = \
        Profile.objects.filter(role__code__in=['teacher', 'manager'], birthday__week=d.isocalendar().week + 1)
    context = {
        "students_coming_birthdays_this_week": students_coming_birthdays_this_week,
        "students_coming_birthdays_next_week": students_coming_birthdays_next_week,
        "teachers_coming_birthdays_this_week": teachers_coming_birthdays_this_week,
        "teachers_coming_birthdays_next_week": teachers_coming_birthdays_next_week,
    }
    return render(request, 'stuff/index.html', context=context)


# Teacher section

@login_required
def get_teacher_list(request):
    teachers = Profile.objects.filter(role__code='teacher', rmv=False)
    context = {
        "teachers": teachers,
    }
    template = loader.get_template('stuff/teacher_list.html')
    return HttpResponse(template.render(context, request))


@login_required
def get_teacher_archive_list(request):
    teachers = Profile.objects.filter(role__code='teacher', rmv=True)
    context = {
        "teachers": teachers,
    }
    template = loader.get_template('stuff/teacher_list.html')
    return HttpResponse(template.render(context, request))


@login_required
def get_filtered_teacher_list(request):
    req = request.GET['req']
    print(req)
    teachers = Profile.objects.filter(role__code='teacher', first_name__icontains=req, rmv=False) | \
        Profile.objects.filter(role__code='teacher', last_name__icontains=req, rmv=False)
    context = {
        "teachers": teachers,
    }
    template = loader.get_template('stuff/teacher_list.html')
    return HttpResponse(template.render(context, request))


@login_required
def teacher_details(request, profile_id):
    teacher = get_object_or_404(Profile, pk=profile_id)
    teacher_id = teacher.teacher.pk
    d = date.today()
    cal = Calendar(year=d.year, month=d.month)
    html_cal = cal.formatmonth(withyear=True, teacher_id=teacher_id)
    calendar = mark_safe(html_cal)
    context = {
        "teacher": teacher,
        "calendar": calendar
    }
    return render(request, 'stuff/teacher.html', context=context)


@login_required
def subjects_per_teacher(request, profile_id):
    teacher_id = get_object_or_404(Profile, pk=profile_id).teacher.pk
    classes = Class.objects.filter(teacher__pk=teacher_id)
    context = {
        "classes": classes,
    }
    template = loader.get_template('stuff/subjects_per_teacher.html')
    return HttpResponse(template.render(context, request))


@login_required
def classes_per_day(request, teacher_id, year, month, day):
    d = date(year, month, day)
    events = Lesson.objects.filter(teacher__pk=teacher_id, date=d).order_by('start_time')
    scheduled_day = ''
    if events:
        for event in events:
            if event.is_complete:
                scheduled_day += f'<tr class="success"><td>{event.student}</td>' \
                                 f'<td>{event.start_time}</td>' \
                                 f'<td></td>' \
                                 f'<td>Проведен</td></tr>'
            elif event.is_cancelled:
                scheduled_day += f'<tr class="warning"><td>{event.student}</td>' \
                                 f'<td>{event.start_time}</td>' \
                                 f'<td></td>' \
                                 f'<td>Отменен</td></tr>'
            elif event.is_moved:
                scheduled_day += f'<tr class="info"><td>{event.student}</td>' \
                                 f'<td>{event.start_time}</td>' \
                                 f'<td>{event.moved_to.date} {event.moved_to.start_time}</td>' \
                                 f'<td>Перенесен</td></tr>'
            else:
                scheduled_day += f'<tr><td>{event.student}</td>' \
                                 f'<td>{event.start_time}</td>' \
                                 f'<td></td>' \
                                 f'<td>По расписанию</td></tr>'
    else:
        scheduled_day += f'<tr class="info text-center">' \
                         f'<td>Занятия нет</td></tr>'
    scheduled_day_html = mark_safe(scheduled_day)
    context = {
        "scheduled_day": scheduled_day_html,
        "d": d,
    }
    template = loader.get_template('stuff/classes_per_day.html')
    return HttpResponse(template.render(context, request))


# Student section

@login_required
def get_student_list(request):
    students = Profile.objects.filter(role__code='student', rmv=False)
    context = {
        "students": students,
    }
    template = loader.get_template('stuff/student_list.html')
    return HttpResponse(template.render(context, request))


@login_required
def get_student_archive_list(request):
    students = Profile.objects.filter(role__code='student', rmv=True)
    context = {
        "students": students
    }
    template = loader.get_template('stuff/student_list.html')
    return HttpResponse(template.render(context, request))


@login_required
def get_filtered_student_list(request):
    req = request.GET['req']
    students = Profile.objects.filter(role__code='student', first_name__icontains=req, rmv=False) | \
        Profile.objects.filter(role__code='student', last_name__icontains=req, rmv=False)
    context = {
        "students": students,
    }
    template = loader.get_template('stuff/student_list.html')
    return HttpResponse(template.render(context, request))


@login_required
def student_details(request, student_id):
    student = get_object_or_404(Profile, pk=student_id)
    context = {"student": student}
    return render(request, 'stuff/student.html', context=context)
