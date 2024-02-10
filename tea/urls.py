from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main-page'),
    path('herbaty', views.AllTeasView.as_view(), name='all-teas'),
    path('herbaty/dodaj', views.TeaCreateView.as_view(), name='create-tea'),
    path('herbaty/<slug:slug>', views.TeaDetailView.as_view(), name='tea-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
