from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'news'
urlpatterns = [
    path('newspage/', views.news_list, name='news_list'),
    path('edit_news/<int:pk>/', views.edit_news, name='edit_news'),
    path('addnews/', views.news_create, name='addnews'),
    path('deletenews/<int:pk>/', views.delete_news, name='delete_news'),
    # path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)