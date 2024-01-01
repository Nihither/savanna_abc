from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.utils.safestring import mark_safe
from datetime import date
from .models import Profile, Class, Lesson, Role, Contact, Teacher, Student
from .forms import AddTeacherForm
from .forms import AddStudentForm
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


@login_required
def add_teacher(request):
    if request.method == 'POST':
        form_data = AddTeacherForm(data=request.POST)
        if form_data.is_valid():
            # creating profile
            new_profile = Profile()
            new_profile.first_name = form_data.cleaned_data['first_name']
            new_profile.last_name = form_data.cleaned_data['last_name']
            new_profile.birthday = form_data.cleaned_data['birthday']
            new_profile.role = Role.objects.get(code='teacher')
            new_profile.save()
            # creating contact
            new_contact = Contact()
            new_contact.profile = new_profile
            new_contact.phone = form_data.cleaned_data['phone']
            new_contact.email = form_data.cleaned_data['email']
            new_contact.additional_contact = form_data.cleaned_data['additional_contact']
            new_contact.additional_contact_description = form_data.cleaned_data['additional_contact_description']
            new_contact.save()
            # creating teacher profile
            new_teacher = Teacher()
            new_teacher.profile = new_profile
            new_teacher.manager = form_data.cleaned_data['manager']
            new_teacher.save()
            return HttpResponse(status=201, content="Сохранено успешно")
        else:
            context = {
                "form": form_data
            }
            template = loader.get_template('stuff/add_teacher.html')
            return HttpResponse(template.render(context, request), status=422)
    else:
        form = AddTeacherForm()
        context = {
            "form": form
        }
        template = loader.get_template('stuff/add_teacher.html')
        return HttpResponse(template.render(context, request))


@login_required
def delete_teacher(request, teacher_id):
    if request.method == 'POST':
        teacher_profile = get_object_or_404(Profile, pk=teacher_id)
        teacher_profile.delete()
        return HttpResponse('Запись удалена')


@login_required
def archive_teacher(request, teacher_id):
    if request.method == 'POST':
        teacher_profile = get_object_or_404(Profile, pk=teacher_id)
        teacher = teacher_profile.teacher
        if teacher_profile.rmv:
            teacher_profile.rmv = False
            teacher_profile.save()
            teacher.rmv = False
            teacher.save()
            return HttpResponse('Перенесено из Архива')
        else:
            teacher_profile.rmv = True
            teacher_profile.save()
            teacher.rmv = True
            teacher.save()
            return HttpResponse('Занесено в Архив')


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


@login_required
def add_student(request):
    if request.method == 'POST':
        form_data = AddStudentForm(data=request.POST)
        if form_data.is_valid():
            # creating profile
            new_profile = Profile()
            new_profile.first_name = form_data.cleaned_data['first_name']
            new_profile.last_name = form_data.cleaned_data['last_name']
            new_profile.birthday = form_data.cleaned_data['birthday']
            new_profile.role = Role.objects.get(code='student')
            new_profile.save()
            # creating contact
            new_contact = Contact()
            new_contact.profile = new_profile
            new_contact.phone = form_data.cleaned_data['phone']
            new_contact.email = form_data.cleaned_data['email']
            new_contact.additional_contact = form_data.cleaned_data['additional_contact']
            new_contact.additional_contact_description = form_data.cleaned_data['additional_contact_description']
            new_contact.save()
            # creating student profile
            new_student = Student()
            new_student.profile = new_profile
            new_student.manager = form_data.cleaned_data['manager']
            new_student.is_adult = form_data.cleaned_data['is_adult']
            new_student.save()
            # creating trustee profile and adding to student profile
            if not new_student.is_adult:
                # creating trustee profile
                new_trustee = Profile()
                new_trustee.first_name = form_data.cleaned_data['trustee_first_name']
                new_trustee.last_name = form_data.cleaned_data['trustee_last_name']
                new_trustee.role = Role.objects.get(code='trustee')
                new_trustee.save()
                # creating trustee contact
                new_trustee_contact = Contact()
                new_trustee_contact.profile = new_trustee
                new_trustee_contact.phone = form_data.cleaned_data['trustee_phone']
                new_trustee_contact.email = form_data.cleaned_data['trustee_email']
                new_trustee_contact.additional_contact = form_data.cleaned_data['trustee_additional_contact']
                new_trustee_contact.additional_contact_description = \
                    form_data.cleaned_data['trustee_additional_contact_description']
                new_trustee_contact.save()
                # adding trustee to student profile
                new_student.trustee = new_trustee
                new_student.save()
            return HttpResponse(status=201, content="Сохранено успешно")
        else:
            context = {
                "form": form_data,
            }
            template = loader.get_template('stuff/add_student.html')
            return HttpResponse(template.render(context, request), status=422)
    else:
        form = AddStudentForm()
        context = {
            "form": form,
        }
        template = loader.get_template('stuff/add_student.html')
        return HttpResponse(template.render(context, request))


@login_required
def delete_student(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(Profile, pk=student_id)
        student.delete()
        return HttpResponse('Запись удалена')


@login_required
def archive_student(request, student_id):
    if request.method == 'POST':
        student_profile = get_object_or_404(Profile, pk=student_id)
        student = student_profile.student
        if student_profile.rmv:
            student_profile.rmv = False
            student_profile.save()
            student.rmv = False
            student.save()
            return HttpResponse('Перенесено из Архива')
        else:
            student_profile.rmv = True
            student_profile.save()
            student.rmv = True
            student.save()
            return HttpResponse('Занесено в Архив')
