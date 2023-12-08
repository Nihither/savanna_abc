from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .models import Profile


@csrf_exempt
def get_profile_uuid(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                user_profile = get_object_or_404(Profile, user=user)
                uuid = user_profile.uuid
                data = {
                    "username": username,
                    "password": password,
                    "uuid": uuid
                }
                return JsonResponse(status=200, data=data)
            else:
                return HttpResponse(status=403, content="User has been disabled")
        else:
            return HttpResponse(status=401, content="Invalid username or password")
