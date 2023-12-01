from django.contrib import admin

from .models import Profile, Role, Contacts, Teacher, Student


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'uuid', 'role_id', 'rmv']
    ordering = ['first_name']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Role)
admin.site.register(Contacts)
admin.site.register(Teacher)
admin.site.register(Student)
