from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


# from persian import PersianDateTime


class tour(models.Model):
    title = models.CharField('Title', max_length=50, null=True, blank=True)
    idtour = models.IntegerField(null=True, blank=True)
    firstdistination = models.CharField(max_length=50, null=True, blank=True)
    lastDestination = models.CharField(max_length=50, null=True, blank=True)
    startdate = models.DateField(null=True, blank=True)
    finishdate = models.DateField(null=True, blank=True)
    capacity = models.IntegerField(default=20000, null=True, blank=True,
                                   validators=[MinValueValidator(0)])  # جلوگیری از اعداد منفی
    clas = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                             related_name='tour_clas')  # اضافه کردن related_name
    image = models.ImageField(upload_to='tourr/', null=True, blank=True)
    price = models.PositiveIntegerField('قیمت',default=1000)  # برای محاسبه هزینه
    # اضافه کردن فیلد جدید برای نوع بلیط
    TICKET_TYPES = [
        ('bus', 'اتوبوس'),
        ('train', 'قطار'),
    ]

    ticket_type = models.CharField(max_length=10, choices=TICKET_TYPES, default='bus')

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tour_profile')  # اضافه کردن related_name
    tours = models.ManyToManyField(tour, blank=True, related_name='tour_profiles')  # اضافه کردن related_name

    def __str__(self):
        return self.user.username


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tour_purchases')  # اضافه کردن related_name
    tour = models.ForeignKey(tour, on_delete=models.CASCADE, related_name='tour_purchases')  # اضافه کردن related_name
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bought {self.tour.title} on {self.purchase_date}"
