from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main-page'),
    path('<slug:slug>', views.TeaDetailView.as_view(), name='tea-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
