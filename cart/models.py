from django.contrib.auth.models import User
from django.db import models
from tour.models import tour
from tourism.models import tourism


# Create your models here.

# سبد خرید
class CartItem(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    tourBuyed = models.ForeignKey(tour, on_delete=models.CASCADE, null=True, blank=True, related_name='cart_tours',db_index=True)
    tourismBuyed = models.ForeignKey(tourism, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='cart_tourisms',db_index=True)
    quantityItem = models.PositiveIntegerField('تعداد', default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        if self.tourBuyed:
            return self.tourBuyed.price * self.quantityItem
        elif self.tourismBuyed:
            return self.tourismBuyed.price_tourism * self.quantityItem
        return 0

    def __str__(self):
        item = self.tourBuyed or self.tourismBuyed
        return f"{self.buyer.username} - {item.title if self.tourBuyed else item.title_tourism} ({self.quantityItem})"


#  سفارش
# cart/models.py
class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(CartItem, related_name='orders')
    total_price = models.DecimalField('جمع کل', max_digits=10, decimal_places=2)
    purchaseDate = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # فقط ذخیره معمولی

    def __str__(self):
        return f"Order {self.id} by {self.buyer.username}"


# class Order(models.Model):
#     buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
#     items = models.ManyToManyField(CartItem, related_name='orders')
#     total_price = models.DecimalField('جمع کل', max_digits=10, decimal_places=2)
#     purchaseDate = models.DateTimeField(auto_now_add=True)
#
#     def save(self, *args, **kwargs):
#         if not self.pk:  # فقط در زمان ایجاد
#             self.total_price = sum(item.get_total() for item in self.items.all())
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return f"Order {self.id} by {self.buyer.username}"


# پرداخت
class Payment(models.Model):
    # One Payment must be for one order.
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    # An image that the buyer uploads.
    payment_image = models.ImageField('عکس پرداخت', upload_to='payments/')
    # An Optional description below the image.
    description = models.TextField('توضیحات', blank=True, null=True)
    """
    is OK Payment or Reject Payment:
    True:OK payment confirmed by the site admin.
    False:Reject Payment not confirmed by the site admin.
    """
    is_verified = models.BooleanField('تأیید شده', default=None,null=True)
    # The admin that verified the Payment.
    verified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                    related_name='verified_payments')
    # The Time that user do the Payment.
    time_payment = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"
