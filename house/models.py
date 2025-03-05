from django.db import models
from django.contrib.auth.models import User

class house(models.Model):
    name_house = models.CharField('Title', max_length=100, null=True, blank=True)
    description_house = models.TextField(null=True, blank=True)
    image_house = models.ImageField(upload_to='tourr/', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_accommodations')

    def __str__(self):
        return self.title if self.title else "Unnamed Accommodation"
