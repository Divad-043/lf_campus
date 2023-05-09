from random import shuffle
from typing import Any
import geoip2.database
import requests
from django import http
from django.conf import settings
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    DetailView,
    UpdateView,
    DeleteView,
    ListView,
    CreateView
)
from .forms import *
from .models import *
from django.contrib.gis.geoip2 import GeoIP2
from .utils import find_nearest_university, get_feature_for_map
from django.contrib import messages


class IndexView(TemplateView):
    template_name = "home/pages/index.html"

    def dispatch(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> http.HttpResponse:
        # Récupérer l'adresse IP de l'utilisateur
        # ip_address = request.META.get('REMOTE_ADDR', None)
        ip_address = requests.get('https://api.ipify.org').text

        if ip_address:
            # Utiliser GeoIP pour récupérer la position de l'utilisateur
            g = GeoIP2()
            city = g.city(ip_address)
            latitude = city['latitude']
            longitude = city['longitude']
            print(city)
            print(latitude, longitude)
        else:
            # Adresse IP non disponible
            print("IP non disponible")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = ItemCategory.objects.all()[:6]
        all_categories = ItemCategory.objects.all()
        deposit_points = DepositPoint.objects.all()[:4]
        if not settings.DEBUG:
            ip_address = self.request.META.get('REMOTE_ADDR')
            # ip_address = self.request.META.get('102.244.42.124')
        else:
            ip_address = requests.get('https://api.ipify.org').text
        reader = geoip2.database.Reader(settings.GEOIP_PATH)
        localisation_response = reader.city(ip_address)
        closest_university = find_nearest_university(localisation_response.location.latitude,
                                                     localisation_response.location.longitude)
        items = ItemQuestionResponse.objects.filter(question__tag__name="name", item__status="Verified")[:10]
        # shuffle(items)
        context["all_categories"] = all_categories
        context['categories'] = categories
        context['items'] = items
        context['deposit_points'] = deposit_points
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        context['localisation_response'] = localisation_response
        context['universities'] = University.objects.all()
        context['closest_university'] = closest_university
        context['feature_for_map'] = get_feature_for_map(items)
        # print(feature_for_map)
        print(context['localisation_response'])
        return context


class DetailItemView(DetailView):
    template_name = "home/pages/detail_item.html"
    model = Item


class ItemListView(ListView):
    model = Item
    template_name = "home/pages/index.html"
    context_object_name = "item_list"

    def get_queryset(self):
        return Item.objects.filter(categories__name="Document")


class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('item_list')
    template_name = "home/pages/add_item.html"
    form_class = ItemForm

    def dispatch(self, request, *args, **kwargs):
        print(self.request.POST)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_type_slug = self.kwargs.get('item_type')
        item_type = get_object_or_404(ItemCategory, slug=item_type_slug)
        category = get_object_or_404(ItemCategory, name=item_type)
        print(category)
        item_questions = category.questions.filter(is_for_reclamation=False)
        print(item_questions)
        ip_address = requests.get('https://api.ipify.org').text
        g = GeoIP2()
        city = g.city(ip_address)
        latitude = city['latitude']
        longitude = city['longitude']
        closest_university = find_nearest_university(latitude, longitude)
        context['item_type'] = item_type
        context['item_questions'] = item_questions
        context['categories'] = ItemCategory.objects.all()
        context['item_type_slug'] = item_type_slug
        context['user_latitude'] = latitude
        context['user_longitude'] = longitude
        context['closest_university'] = closest_university
        return context

    def form_valid(self, form):
        item = form.save(commit=False)
        item_type_slug = self.kwargs.get('item_type')
        item_type = get_object_or_404(ItemCategory, slug=item_type_slug)
        category = get_object_or_404(ItemCategory, name=item_type)
        item.category = category
        found_location_longitude = float(self.request.POST['found_location_longitude'])
        found_location_latitude = float(self.request.POST['found_location_latitude'])
        item.first_image = self.request.FILES.get('first_image')
        item.second_image = self.request.FILES.get('second_image')
        item.found_location_longitude = found_location_longitude
        item.found_location_latitude = found_location_latitude
        if self.request.user.is_authenticated:
            item.founder = self.request.user
        else:
            visitor_first_name = form.cleaned_data.get('first_name')
            visitor_last_name = form.cleaned_data.get('last_name')
            visitor_email = form.cleaned_data.get('email')
            visitor_phone = form.cleaned_data.get('phone')
            visitor = Visitor.objects.create(first_name=visitor_first_name, last_name=visitor_last_name,
                                             email=visitor_email, phone=visitor_phone)
            item.added_by_visitor = visitor
        item.save()
        # category = form.cleaned_data.get('categories')
        category_questions = category.questions.all()
        print(category_questions)
        for question in category_questions:
            print(question.tag.name)
            answer = self.request.POST[str(question.tag.name)]
            ItemQuestionResponse.objects.create(category=category, question=question, answer=answer, item=item)
        messages.success(self.request, "Item add successfully !!!")
        return redirect('core:index')


class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('item_list')


class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy('item_list')


class ItemDetailView(DetailView):
    model = Item
    template_name = "home/pages/detail_item.html"

    def dispatch(self, request, *args, **kwargs):
        print("test_dispatch")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        print("test_get_context")
        context = super().get_context_data(**kwargs)
        context['test'] = 'test'
        other_item_information = ItemQuestionResponse.objects.filter(item=self.object)
        item_question_tag_for_name = other_item_information.filter(question__tag__name="Name").first()
        item_name = item_question_tag_for_name
        context['other_item_information'] = other_item_information
        context['item_name'] = item_name
        context['mapbox_access_token'] = settings.MAPBOX_ACCESS_TOKEN
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        return context


class ItemSearchView(ListView):
    model = Item
    template_name = "home/pages/item_listing_map_grid_view.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        location = self.request.GET.get('location')
        category = self.request.GET.get('category')
        keyword = self.request.GET.get('keyword')
        if location:
            queryset = queryset.filter(Q(found_location_name__icontains=location) | Q(
                lost_location_name__icontains=location))
        if category:
            queryset = queryset.filter(category__name=category)
        if keyword:
            queryset = queryset.filter(itemquestionresponse__answer__icontains=keyword)

        print(queryset)
        return queryset.distinct()


class ItemExploreByCategoryView(ListView):
    # template_name = 'home/pages/item_by_category.html'
    template_name = 'home/pages/item_listing_map_grid_view.html'
    queryset = ItemQuestionResponse.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        item_type = self.kwargs.get('item_type')
        queryset = ItemQuestionResponse.objects.filter(item__category__name=item_type)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ItemCategory.objects.all()
        return context


class ExploreByUniversityView(ListView):
    template_name = 'home/pages/item_listing_map_grid_view.html'
    model = Item

    def get_queryset(self):
        queryset = super().get_queryset()
        university_slug = self.kwargs.get('university_slug')
        university = get_object_or_404(University, slug=university_slug)
        queryset = queryset.filter(deposit_point__associate_university=university)
        return queryset.distinct()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        university_slug = self.kwargs.get('university_slug')
        university = get_object_or_404(University, slug=university_slug)
        items = ItemQuestionResponse.objects.filter(item__deposit_point__associate_university=university)
        context['items'] = items
        context['university'] = university
        context['feature_for_map'] = get_feature_for_map(items)
        return context


class ExploreByDepositPoint(ListView):
    template_name = 'home/pages/item_listing_map_grid_view.html'


class DepositPointListView(ListView):
    model = DepositPoint
    template_name = "home/pages/deposit_point_list.html"
    context_object_name = "deposit_point_list"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class DepositPointCreateView(CreateView):
    model = DepositPoint
    form_class = DepositPointForm
    success_url = reverse_lazy('deposit_point_list')
    template_name = "home/pages/add_deposit_point.html"


class DepositPointUpdateView(UpdateView):
    model = DepositPoint
    form_class = DepositPointForm
    success_url = reverse_lazy('deposit_point_list')
    template_name = "home/pages/add_deposit_point.html"


class DepositPointDeleteView(DeleteView):
    model = DepositPoint
    success_url = reverse_lazy('deposit_point_list')
    template_name = "home/pages/delete_deposit_point.html"


class DepositPointDetailView(DetailView):
    model = DepositPoint
    template_name = "home/pages/detail_deposit_point.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mapbox_access_token'] = settings.MAPBOX_ACCESS_TOKEN
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        return context


class DepositPointSearchView(ListView):
    model = DepositPoint
    template_name = "home/pages/deposit_point_search.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(Q(location_name__icontains=location))
        return queryset.distinct()


class DepositPointExploreView(ListView):
    model = DepositPoint
    template_name = "home/pages/deposit_point_explore.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.kwargs.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset.distinct()
