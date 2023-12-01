from django.http import JsonResponse
from django.views import View
from .models import News


class NewsListView(View):
    def get(self, request):
        news_list = News.objects.all()
        news_list_serialized = []
        for news_item in news_list:
            news_item_data = {
                "id": news_item.pk,
                "title": news_item.title,
                "text": news_item.text,
                "image_url": news_item.image.url,
                "createdDate": news_item.createdDate
            }
            news_list_serialized.append(news_item_data)
        data = {
            "news": news_list_serialized
        }
        return JsonResponse(data=data)


class NewsItemView(View):
    def get(self, request, news_id):
        news_item = News.objects.get(pk=news_id)
        data = {
            "id": news_item.pk,
            "title": news_item.title,
            "text": news_item.text,
            "image_url": news_item.image.url,
            "createdDate": news_item.createdDate
        }
        return JsonResponse(data=data)
