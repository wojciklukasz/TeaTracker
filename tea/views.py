from typing import Any

from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .forms import TeaForm
from .models import Profile, Tea

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


class TeaCreateView(CreateView):
    model = Tea
    form_class = TeaForm
    template_name = 'tea/create-tea.html'

    def form_valid(self, form: TeaForm) -> HttpResponse:
        profile = Profile.objects.get(id=1)

        slug = slugify(form.instance.name)
        if Tea.objects.filter(name=form.instance.name):
            slug = slug + f'_{len(Tea.objects.filter(name=form.instance.name))}'

        form.instance.profile = profile
        form.instance.slug = slug

        self.success_url = reverse_lazy(
            'tea-detail',
            kwargs={
                'slug': slug,
            },
        )

        return super().form_valid(form)
