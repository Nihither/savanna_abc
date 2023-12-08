from django.urls import path
from .api import get_chats_list


# API urls
api_url_patterns = [
    path('get_chats_list/', get_chats_list, name='get_chats_list')
]
