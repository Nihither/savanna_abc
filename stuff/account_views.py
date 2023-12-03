from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .accouts_forms import CustomPasswordResetForm, CustomSetPasswordForm, CustomPasswordChangeForm


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if request.POST.get('next') == 'None':
            redirect_to = '/'
        else:
            redirect_to = request.POST.get('next')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user=user)
                return HttpResponseRedirect(redirect_to=redirect_to)
            else:
                return HttpResponse("Account has been disabled")
        else:
            return HttpResponse("Invalid login details supplied.")
    elif request.method == 'GET':
        redirect_to = request.GET.get('next')
        return render(request, 'accounts/login.html', {'next': redirect_to, })


def user_logout(request, next):
    if request.method == 'POST':
        redirect_to = request.POST.get('next')
        confirm = request.POST.get('submit')
        if confirm == 'Logout':
            logout(request)
            return HttpResponseRedirect(redirect_to='/accounts/login')
        else:
            return HttpResponseRedirect(redirect_to=redirect_to)
    elif request.method == 'GET':
        redirect_to = next
        return render(request, 'accounts/logout.html', {'next': redirect_to, })


class PasswordChange(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


class PasswordReset(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_email_subject.txt'
    form_class = CustomPasswordResetForm


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = CustomSetPasswordForm


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
