from django.urls import path

from .api import NewsListView, NewsItemView


# Api urls
api_url_patterns = [
    path('all/', NewsListView.as_view(), name='news_list'),
    path('<int:news_id>/', NewsItemView.as_view(), name='news_item')
]

# Views urls
views_url_patterns = [

]
