from django.contrib import admin
from .models import Chat, Message


# Register your models here.
class ChatAdmin(admin.ModelAdmin):
    list_display = ['uuid']
    ordering = ['uuid']


class MessageAdmin(admin.ModelAdmin):
    list_display = ['chat', 'sender']
    ordering = ['created_date']


admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
