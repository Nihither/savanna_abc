from django.urls import path
from .views import index
from .views import get_teacher_list, get_teacher_archive_list, get_filtered_teacher_list, teacher_details, \
    subjects_per_teacher, classes_per_day
from .views import get_student_list, get_student_archive_list, get_filtered_student_list, student_details
from .account_views import user_login, user_logout, PasswordReset, PasswordResetDone, PasswordResetConfirm, \
    PasswordResetComplete, PasswordChange, PasswordChangeDone
from .accounts_api import get_profile_uuid
from .scheduler import birthday_notification


# API urls
api_url_patterns = []

# Views urls
views_url_patterns = [
    path('', index, name='index'),
    # teachers
    path('teacher/list/', get_teacher_list, name='teacher_list'),
    path('teacher/list/archive/', get_teacher_archive_list, name='teacher_archive_list'),
    path('teacher/search/', get_filtered_teacher_list, name='teacher_search_results'),
    path('teacher/<int:profile_id>/', teacher_details, name='teacher_details'),
    path('teacher/<int:profile_id>/students/', subjects_per_teacher, name='subjects_per_teacher'),
    path('teacher/<int:teacher_id>/<int:year>/<int:month>/<int:day>/', classes_per_day, name='classes_per_day'),
    # students
    path('student/list/', get_student_list, name='student_list'),
    path('student/list/archive/', get_student_archive_list, name='student_archive_list'),
    path('student/search/', get_filtered_student_list, name='student_search_result'),
    path('student/<int:student_id>/', student_details, name='student_details'),
]

# Account API urls
accounts_api_url_patterns = [
    path('get_profile_uuid/', get_profile_uuid, name='get_profile_uuid')
]

# Account urls
accounts_url_patterns = [
    path('login/', user_login, name='login'),
    path('logout/next=<path:next>', user_logout, name='logout'),
    path('password_reset/', PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done', PasswordResetDone.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<idb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('password_change/', PasswordChange.as_view(), name='password_change'),
    path('password_change/done', PasswordChangeDone.as_view(), name='password_change_done'),
]

scheduler_url_patterns = [
    path('birthday_notification/', birthday_notification)
]
