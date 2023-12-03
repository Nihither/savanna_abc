"""savanna URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from news import urls as news_urls
from stuff import urls as stuff_urls
from messenger import urls as messenger_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(stuff_urls.accounts_url_patterns)),
    path('api/news/', include(news_urls.api_url_patterns)),
    path('news/', include(news_urls.views_url_patterns)),
    path('api/stuff/', include(stuff_urls.api_url_patterns)),
    path('stuff/', include(stuff_urls.views_url_patterns)),
    path('api/chats/', include(messenger_urls.api_url_patterns))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
