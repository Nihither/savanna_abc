from django.contrib import admin

from .models import Profile, Role, Contact, Teacher, Student


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'uuid', 'role_id', 'rmv']
    ordering = ['first_name']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Role)
admin.site.register(Contact)
admin.site.register(Teacher)
admin.site.register(Student)
