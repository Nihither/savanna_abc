from django.urls import path
from .api import get_chats_list, get_messages_list


# API urls
api_url_patterns = [
    path('get_chats_list/', get_chats_list, name='get_chats_list'),
    path('get_messages_list/', get_messages_list, name='get_message_list')
]
