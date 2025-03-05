# ---------------------------------------این ها درست بودن👇_______________________________________
from django.contrib import admin
from django.urls import path, include
from tour import views as tour_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", tour_views.main_page, name='main_page'),
    path('accounts2/', include('accounts.urls')),

    #     برای اضافه کردن اپشن ورود با گوگل👇
    path('accounts/', include('allauth.urls')),
    # path("/", include("users.urls")),
    #     برای اضافه کردن اپشن ورود با گوگل 👆

    path("tour/", include("tour.urls")),
    path('tourism/', include('tourism.urls')),
    path('news/', include('news.urls')),
    path('house/', include('house.urls')),
    path('media/<str:rootFolder>/<str:fileName>', views.returnImgResponse, name="returnImgResponse"),
    # path('testapp/', include('testapp.urls'))
]
# ---------------------------------------این ها درست بودن👆_______________________________________
