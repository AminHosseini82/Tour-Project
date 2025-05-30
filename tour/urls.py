from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'tour'
urlpatterns = [
    path('homepage/', views.home_view, name='homepage'),
    path('mainpage/', views.main_page, name='main_page'),  # صفحه اصلی
    path('edittour/<int:pk>/', views.edittour, name='edittour'),
    path('add/', views.tour_create, name='add'),
    path('deletetour/<int:pk>/', views.deletetour, name='deletetour'),
    # path('search/', search, name='search'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('buy/<int:tour_id>/', views.buy_tour, name='buy_tour'),  # URL برای خرید
    path('profile/', views.profile_view, name='profile_view'),  # URL برای پروفایل کاربر


#     the all safario html

    path('amenities/', views.amenities_page_view, name='amenities'),  # نام 'amenities' را برای این URL انتخاب کردیم

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)