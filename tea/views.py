from typing import Any

from django.db.models.query import QuerySet
from django.views.generic import ListView

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
        queryset_dict = {
            'recent': queryset_recent,
            'random': queryset_random,
        }

        return queryset_dict
