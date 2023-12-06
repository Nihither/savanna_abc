from django.urls import path
from .views import index
from .account_views import user_login, user_logout, PasswordReset, PasswordResetDone, PasswordResetConfirm, \
    PasswordResetComplete, PasswordChange, PasswordChangeDone
from .accounts_api import get_profile_uuid


# API urls
api_url_patterns = []

# Views urls
views_url_patterns = [
    path('', index, name='index')
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
