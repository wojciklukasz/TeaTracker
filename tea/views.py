from typing import Any

from django.db.models.query import QuerySet
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Tea

# Create your views here.


class MainPageView(ListView):
    template_name = 'tea/main-page.html'
    model = Tea
    context_object_name = 'teas'
    ordering = ['-date_added']

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset_recent = queryset[:3]
        queryset_random = Tea.objects.all().order_by('?')[:3]
        queryset_last_viewed = Tea.objects.all().order_by('-last_viewed')[:3]
        queryset_dict = {
            'recent': queryset_recent,
            'random': queryset_random,
            'last_viewed': queryset_last_viewed,
        }

        return queryset_dict


class TeaDetailView(DetailView):
    model = Tea
    template_name = 'tea/tea-detail.html'


class AllTeasView(ListView):
    template_name = 'tea/all-teas.html'
    model = Tea
    context_object_name = 'teas'
    ordering = ['-date_added']
