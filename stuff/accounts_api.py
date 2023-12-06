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
                return HttpResponse("User has been disabled", status=403)
        else:
            return HttpResponse("Invalid username or password", status=401)
