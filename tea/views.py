from typing import Any

from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from . import forms, models

# Create your views here.

generic_template = 'tea/create-others.html'


class MainPageView(ListView):
    template_name = 'tea/main-page.html'
    model = models.Tea
    context_object_name = 'teas'
    ordering = ['-date_added']

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset_recent = queryset[:3]
        queryset_random = self.model.objects.all().order_by('?')[:3]
        queryset_last_viewed = self.model.objects.all().order_by('-last_viewed')[:3]
        queryset_dict = {
            'recent': queryset_recent,
            'random': queryset_random,
            'last_viewed': queryset_last_viewed,
        }

        return queryset_dict


class TeaDetailView(DetailView):
    model = models.Tea
    template_name = 'tea/tea-detail.html'


class AllTeasView(ListView):
    template_name = 'tea/all-teas.html'
    model = models.Tea
    context_object_name = 'teas'
    ordering = ['-date_added']


class TeaCreateView(CreateView):
    model = models.Tea
    form_class = forms.TeaForm
    template_name = 'tea/create-tea.html'

    def form_valid(self, form: forms.TeaForm) -> HttpResponse:
        profile = models.Profile.objects.get(id=1)

        slug = slugify(form.instance.name)
        if self.model.objects.filter(name=form.instance.name):
            slug = slug + f'-{len(self.model.objects.filter(name=form.instance.name))}'

        form.instance.profile = profile
        form.instance.slug = slug

        self.success_url = reverse_lazy(
            'tea-detail',
            kwargs={
                'slug': slug,
            },
        )

        return super().form_valid(form)


class StoreCreateView(CreateView):
    model = models.Store
    form_class = forms.StoreForm
    template_name = generic_template
    success_url = reverse_lazy('create-tea')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Nowy sklep'
        return context


class TypeCreateView(CreateView):
    model = models.Type
    form_class = forms.TypeForm
    template_name = generic_template
    success_url = reverse_lazy('create-tea')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Nowy typ herbaty'
        return context


class CultivarCreateView(CreateView):
    model = models.Cultivar
    form_class = forms.CultivarForm
    template_name = generic_template
    success_url = reverse_lazy('create-tea')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Nowy kultywar'
        return context


class CountryCreateView(CreateView):
    model = models.Country
    form_class = forms.CountryForm
    template_name = generic_template
    success_url = reverse_lazy('create-tea')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Nowy kraj'
        return context


class ProvinceCreateView(CreateView):
    model = models.Province
    form_class = forms.ProvinceForm
    template_name = generic_template
    success_url = reverse_lazy('create-tea')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Nowa prowincja'
        return context


class RegionCreateView(CreateView):
    model = models.Region
    form_class = forms.RegionForm
    template_name = generic_template
    success_url = reverse_lazy('create-tea')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Nowy region'
        return context
