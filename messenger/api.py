from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from stuff.models import Profile
from .models import Chat


@csrf_exempt
def get_chats_list(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        uuid = request.POST.get('uuid')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                user_profile = Profile.objects.get(uuid=uuid)
                chats = Chat.objects.filter(participants=user_profile, rmv=False)
                chats_data = []
                for chat in chats:
                    chat_data = {
                        "uuid": chat.uuid
                    }
                    if chat.name:
                        chat_data["name"] = chat.name
                    else:
                        participants = chat.participants.all()
                        for profile in participants:
                            if profile != user_profile:
                                part_data = {
                                    "participant": profile.full_name()
                                }
                                chat_data.update(part_data)
                    chats_data.append(chat_data)
                json_data = {
                    "chats": chats_data
                }
                return JsonResponse(status=200, data=json_data)
            else:
                return HttpResponse(status=403, content="Forbidden")
        else:
            return HttpResponse(status=401, content="Invalid name or password")
