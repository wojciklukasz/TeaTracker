from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainPageView, name='main-page'),
]
