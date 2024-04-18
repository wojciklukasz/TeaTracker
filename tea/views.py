from __future__ import annotations

from typing import Any, Dict

from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.text import slugify
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView

from . import forms, models

# Create your views here.

generic_template = "tea/create-others.html"


class MainPageView(ListView):
    template_name = "tea/main-page.html"
    model = models.Tea
    context_object_name = "teas"
    ordering = ["-date_added"]

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.session.get("profile_id"):
            return redirect("profile-select")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset = queryset.filter(profile__id=self.request.session.get("profile_id"))
        queryset_recent = queryset[:3]
        queryset_random = self.model.objects.filter(
            profile__id=self.request.session.get("profile_id")
        ).order_by("?")[:3]
        queryset_last_viewed = queryset.order_by("-last_viewed")[:3]
        queryset_dict = {
            "recent": queryset_recent,
            "random": queryset_random,
            "last_viewed": queryset_last_viewed,
        }

        return queryset_dict


class ProfileSelectView(FormView):
    model = models.Profile
    template_name = "tea/profile.html"
    form_class = forms.ProfileSelectForm
    success_url = reverse_lazy("main-page")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if not self.request.session.get("profile_id"):
            context["current_profile"] = None
        else:
            profile_id = self.request.session.get("profile_id")
            context["current_profile"] = models.Profile.objects.get(id=profile_id)
        return context

    def form_valid(self, form):
        self.request.session["profile_id"] = form.cleaned_data["profile"].id
        return super().form_valid(form)


class ProfileCreateView(CreateView):
    model = models.Profile
    template_name = generic_template
    form_class = forms.ProfileForm
    success_url = reverse_lazy("profile-select")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Nowy profil"
        return context


class AllTeasView(ListView):
    template_name = "tea/all-teas.html"
    model = models.Tea
    context_object_name = "teas"
    ordering = ["-date_added"]

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.session.get("profile_id"):
            return redirect("profile-select")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        querryset = super().get_queryset()
        return querryset.filter(profile__id=self.request.session.get("profile_id"))


class TeaDetailView(DetailView):
    model = models.Tea
    template_name = "tea/tea-detail.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.session.get("profile_id"):
            return redirect("profile-select")
        return super().dispatch(request, *args, **kwargs)

    def get(
        self, request: HttpRequest, slug: str, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        tea = models.Tea.objects.get(slug=slug)
        tea.last_viewed = timezone.now()
        tea.save()
        return super().get(request, *args, **kwargs)


class TeaCreateView(CreateView):
    model = models.Tea
    form_class = forms.TeaForm
    template_name = "tea/create-tea.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["button_text"] = "Dodaj"
        return context

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.session.get("profile_id"):
            return redirect("profile-select")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: forms.TeaForm) -> HttpResponse:
        profile_id = self.request.session.get("profile_id")
        profile = models.Profile.objects.get(id=profile_id)

        slug = slugify(form.instance.name)
        if self.model.objects.filter(name=form.instance.name):
            slug = slug + f"-{len(self.model.objects.filter(name=form.instance.name))}"

        form.instance.profile = profile
        form.instance.slug = slug

        self.success_url = reverse_lazy(
            "tea-detail",
            kwargs={
                "slug": slug,
            },
        )

        return super().form_valid(form)


class TeaUpdateView(UpdateView):
    model = models.Tea
    template_name = "tea/create-tea.html"
    fields = [
        "name",
        "price_per_100_grams",
        "grams_left",
        "season",
        "year",
        "harvest_date",
        "store",
        "type",
        "cultivar",
        "country",
        "province",
        "region",
        "store_description",
        "user_description",
        "tasting_notes",
        "additional_notes",
    ]

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["button_text"] = "Zapisz zmiany"
        return context

    def get_success_url(self) -> str:
        print(self.object.slug)
        return reverse_lazy("tea-detail", kwargs={"slug": self.object.slug})


class StoreCreateView(CreateView):
    model = models.Store
    form_class = forms.StoreForm
    template_name = generic_template
    success_url = reverse_lazy("create-tea")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.session.get("profile_id"):
            return redirect("profile-select")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Nowy sklep"
        return context


class TypeCreateView(CreateView):
    model = models.Type
    form_class = forms.TypeForm
    template_name = generic_template
    success_url = reverse_lazy("create-tea")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.session.get("profile_id"):
            return redirect("profile-select")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Nowy typ herbaty"
        return context


class CultivarCreateView(CreateView):
    model = models.Cultivar
    form_class = forms.CultivarForm
    template_name = generic_template
    success_url = reverse_lazy("create-tea")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.session.get("profile_id"):
            return redirect("profile-select")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Nowy kultywar"
        return context


class CountryCreateView(CreateView):
    model = models.Country
    form_class = forms.CountryForm
    template_name = generic_template
    success_url = reverse_lazy("create-tea")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.session.get("profile_id"):
            return redirect("profile-select")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Nowy kraj"
        return context


class ProvinceCreateView(CreateView):
    model = models.Province
    form_class = forms.ProvinceForm
    template_name = generic_template
    success_url = reverse_lazy("create-tea")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.session.get("profile_id"):
            return redirect("profile-select")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Nowa prowincja"
        return context


class RegionCreateView(CreateView):
    model = models.Region
    form_class = forms.RegionForm
    template_name = generic_template
    success_url = reverse_lazy("create-tea")

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.session.get("profile_id"):
            return redirect("profile-select")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Nowy region"
        return context


class BrewCreateView(CreateView):
    model = models.Brew
    form_class = forms.BrewForm
    template_name = "tea/create-brew.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.session.get("profile_id"):
            return redirect("profile-select")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: forms.BrewForm) -> HttpResponse:
        tea_slug = self.kwargs["slug"]
        tea = models.Tea.objects.get(slug=tea_slug)

        form.instance.tea = tea

        if form.instance.grams and form.instance.water_ml:
            form.instance.ratio = 100 / form.instance.water_ml * form.instance.grams

        self.success_url = reverse_lazy(
            "tea-detail",
            kwargs={
                "slug": tea_slug,
            },
        )

        return super().form_valid(form)


class BrewListView(ListView):
    template_name = "tea/brews-list.html"
    model = models.Brew
    context_object_name = "brews"
    ordering = ["brew_date"]

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.session.get("profile_id"):
            return redirect("profile-select")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        tea_slug = self.kwargs["slug"]
        tea = models.Tea.objects.get(slug=tea_slug)

        querryset = super().get_queryset()
        querryset = querryset.filter(tea=tea)

        return querryset.filter(tea=tea)


class BrewDetailView(DetailView):
    model = models.Brew
    template_name = "tea/brew-detail.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.session.get("profile_id"):
            return redirect("profile-select")
        return super().dispatch(request, *args, **kwargs)
