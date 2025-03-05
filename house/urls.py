from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'house'
urlpatterns = [
    path('newspage/', views.house_list, name='house_list'),
    path('edit_house/<int:pk>/', views.edit_house, name='edit_houses'),
    path('addnews/', views.house_create, name='add_houses'),
    path('delete_house/<int:pk>/', views.delete_house, name='delete_houses'),
    # path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)