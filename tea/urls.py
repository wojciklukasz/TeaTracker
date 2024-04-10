from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.MainPageView.as_view(), name="main-page"),
    path("profil", views.ProfileSelectView.as_view(), name="profile-select"),
    path("profil/dodaj", views.ProfileCreateView.as_view(), name="create-profile"),
    path("herbaty", views.AllTeasView.as_view(), name="all-teas"),
    path("herbaty/dodaj", views.TeaCreateView.as_view(), name="create-tea"),
    path("herbaty/dodaj/sklep", views.StoreCreateView.as_view(), name="create-store"),
    path("herbaty/dodaj/typ", views.TypeCreateView.as_view(), name="create-type"),
    path(
        "herbaty/dodaj/kultywar",
        views.CultivarCreateView.as_view(),
        name="create-cultivar",
    ),
    path(
        "herbaty/dodaj/kraj", views.CountryCreateView.as_view(), name="create-country"
    ),
    path(
        "herbaty/dodaj/prowincja",
        views.ProvinceCreateView.as_view(),
        name="create-province",
    ),
    path(
        "herbaty/dodaj/region", views.RegionCreateView.as_view(), name="create-region"
    ),
    path("herbaty/<slug:slug>", views.TeaDetailView.as_view(), name="tea-detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
