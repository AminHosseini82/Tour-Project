from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('upload-payment/<int:order_id>/', views.upload_payment, name='upload_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('admin/review-payments/', views.admin_payment_review, name='admin_payment_review'),
    path('admin/reject-payment/<int:payment_id>/', views.reject_payment_message, name='reject_payment_message'),
    # this is for error showwing in def reject_payment_message
    path('no-phone-number/', no_phone_number_error, name='no_phone_number_error'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
