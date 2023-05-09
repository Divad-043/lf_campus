from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    DetailView,
    UpdateView,
    DeleteView,
    ListView,
    CreateView
)
from .models import *
from .forms import *


class IndexView(TemplateView):
    template_name = "dashboard/pages/index.html"


class ChatView(TemplateView):
    template_name = "dashboard/pages/chat.html"


class ItemIdentifierListViewForUser(ListView):
    model = ItemIdentifier
    template_name = "dashboard/pages/item_identifier_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class ItemIdentifierCreateView(CreateView):
    model = ItemIdentifier
    form_class = ItemIdentifierForm
    success_url = reverse_lazy('item_identifier_list')
    template_name = "dashboard/pages/add_item_identifier.html"


class ItemIdentifierUpdateView(UpdateView):
    model = ItemIdentifier
    form_class = ItemIdentifierForm
    success_url = reverse_lazy('item_identifier_list')
    template_name = "dashboard/pages/add_item_identifier.html"


class ItemIdentifierDeleteView(DeleteView):
    model = ItemIdentifier
    success_url = reverse_lazy('item_identifier_list')
    template_name = "dashboard/pages/delete_item_identifier.html"


class ItemIdentifierDetailView(DetailView):
    model = ItemIdentifier
    template_name = "dashboard/pages/item_identifier_detail.html"