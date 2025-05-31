from django.urls import path
from . import views
from django.conf import settings

app_name = 'tourism'
urlpatterns = [
    path('tourism/', views.tourism_view, name='tourismpage'),
    path('mainpagee/', views.main_page, name='main_page'),  # صفحه اصلی
    path('edittourism/<int:pk>/', views.edittourism, name='edittourism'),
    path('addtourism/', views.tourism_create, name='addtourism'),
    path('deletetourism/<int:pk>/', views.deletetourism, name='deletetourism'),
    path('tourism/<int:tourism_id>/', views.tourism_detail, name='tourism_detail'),
    path('buy/<int:tourism_id>/', views.buy_tourism, name='buy_tourism'),
    path('profile/', views.profile_view, name='profile_view'),  # URL برای پروفایل کاربر
]
