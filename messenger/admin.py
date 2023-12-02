from django.contrib import admin

from .models import Chat


# Register your models here.
class ChatAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'first_person', 'second_person']
    ordering = ['uuid']


admin.site.register(Chat, ChatAdmin)
