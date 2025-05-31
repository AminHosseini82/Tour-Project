from django.db import models
from django.contrib.auth.models import User

class News(models.Model):
    title_news = models.CharField('Title', max_length=50, null=True, blank=True)
    description_news = models.TextField(null=True, blank=True)  # افزایش طول توصیف
    image_news = models.ImageField(upload_to='tourr/', null=True, blank=True)  # تغییر نام پوشه به news
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_news')  # ارتباط با مدل کاربر

    def __str__(self):
        return self.title_news