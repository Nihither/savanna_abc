from django.contrib import admin
from .models import News


# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    list_display = ['title']
    ordering = ['createdDate']


admin.site.register(News, NewsAdmin)
