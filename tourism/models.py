from time import timezone
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
# from persian import PersianDateTime


#
# class tourism(models.Model):
#     title = models.CharField('Title', max_length=50, null=True, blank=True)  # می‌تواند نال باشد
#     description = models.CharField(max_length=50, null=True, blank=True)  # می‌تواند نال باشد
#     firstdistination = models.CharField(max_length=50, null=True, blank=True)  # می‌تواند نال باشد
#     lastDestination = models.CharField(max_length=50, null=True, blank=True)  # می‌تواند نال باشد
#     startdate = models.DateField(null=True, blank=True)  # می‌تواند نال باشد
#     # finishdate = models.DateField(null=True, blank=True)  # می‌تواند نال باشد
#     capacity = models.IntegerField(default=20000, null=True, blank=True,)  # جلوگیری از اعداد منفی
#     clas = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     # clas = models.ForeignKey(User, on_delete=models.CASCADE)  # فیلد ForeignKey به User
#     image = models.ImageField(upload_to='tour/', null=True, blank=True)  # فیلد عکس
#
#
# objects = models.Manager()
#
#
# def __str__(self):
#         return self.title
#
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, )
#     tours = models.ManyToManyField(tourism, blank=True)
#
#     def __str__(self):
#         return self.user.username
#
#
# class Purchase(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     tour = models.ForeignKey(tourism, on_delete=models.CASCADE)
#     purchase_date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.user.username} bought {self.tourism.title} on {self.purchase_date}"



class tourism(models.Model):
    title_tourism = models.CharField('Title', max_length=50, null=True, blank=True)
    description = models.CharField(max_length=50, null=True, blank=True)
    firstdistination_tourism = models.CharField(max_length=50, null=True, blank=True)
    lastDestination = models.CharField(max_length=50, null=True, blank=True)
    startdate_tourism = models.DateField(null=True, blank=True)
    capacity_tourism = models.IntegerField(default=20000, null=True, blank=True, validators=[MinValueValidator(0)])  # جلوگیری از اعداد منفی
    clas = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='tourism_clas')  # اضافه کردن related_name
    image_tourism = models.ImageField(upload_to='tour/', null=True, blank=True)
    price_tourism =models.IntegerField(null=True, blank=True)
    # اضافه کردن فیلد جدید برای نوع بلیط
    TICKET_TYPES = [
        ('bus', 'اتوبوس'),
        ('train', 'قطار'),
    ]

    ticket_typetourism = models.CharField(max_length=10, choices=TICKET_TYPES, default='bus')

    def __str__(self):
        return self.title_tourism

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tourism_profile')  # اضافه کردن related_name
    tours = models.ManyToManyField(tourism, blank=True, related_name='tourism_profiles')  # اضافه کردن related_name

    def __str__(self):
        return self.user.username

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tourism_purchases')  # اضافه کردن related_name
    tour = models.ForeignKey(tourism, on_delete=models.CASCADE, related_name='tourism_purchases')  # اضافه کردن related_name
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bought {self.tour.title_tourism} on {self.purchase_date}"