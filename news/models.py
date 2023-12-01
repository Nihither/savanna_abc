from django.db import models


# Create your models here.
class News(models.Model):
    title = models.CharField(verbose_name="Название", max_length=200)
    text = models.TextField(verbose_name="Текст", max_length=1000)
    image = models.ImageField(verbose_name="Изображение", upload_to='news', blank=True)
    createdDate = models.DateTimeField(verbose_name="Создано", auto_created=True)
