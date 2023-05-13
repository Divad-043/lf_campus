from django.shortcuts import render, redirect
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
from django.db.models import Q
from random import shuffle
from .models import *
from .models import *


class IndexView(TemplateView):
    template_name = "home/pages/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = ItemCategory.objects.all()[:6]
        all_categories = ItemCategory.objects.all()
        deposit_points = DepositPoint.objects.all()[:4]
        items = []
        for category in categories:
            items += list(Item.objects.filter(categories=category)[:10])
        shuffle(items)
        context["all_categories"] = all_categories
        context['categories'] = categories
        context['items'] = items
        context['deposit_points'] = deposit_points
        return context


class DetailItemView(TemplateView):
    template_name = "home/page/detail_item.html"


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

    def form_valid(self, form):
        item = form.save(commit=False)
        item.save()
        category = form.cleaned_data.get('categories')
        category_questions = category.questions.all()

        # Pour chaque question liée à la catégorie, créer une réponse liée à l'objet Item créé
        for question in category_questions:
            answer = form.cleaned_data.get(question.question)
            ItemQuestionResponse.objects.create(category=category, question=question, answer=answer, item=item)

        return redirect('item-detail', pk=item.pk)


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


class ItemSearchView(ListView):
    model = Item
    template_name = "main/item_search.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        # Récupération des paramètres de recherche
        location = self.request.GET.get('location')
        category = self.request.GET.get('category')
        keyword = self.request.GET.get('keyword')

        # Filtrage par localisation
        if location:
            queryset = queryset.filter(Q(location__icontains=location) | Q(found_location__icontains=location) | Q(lost_location__icontains=location))

        # Filtrage par catégorie
        if category:
            queryset = queryset.filter(categories__name=category)

        # Filtrage par mot-clé
        if keyword:
            queryset = queryset.filter(itemquestionresponse__answer__icontains=keyword)

        return queryset.distinct()