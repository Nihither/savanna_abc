from django.contrib import admin
from .models import Profile, Role, Contact, Teacher, Student, Class, Lesson


# Register your models here.
class ContactInLine(admin.StackedInline):
    model = Contact
    extra = 1


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'uuid', 'role_id', 'rmv']
    ordering = ['first_name']
    inlines = [ContactInLine]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Role)
admin.site.register(Contact)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Lesson)
