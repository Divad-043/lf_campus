from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, UpdateView, DeleteView

# Create your views here.
class IndexView(TemplateView):
    template_name = "main/index.html"


class DetailItemView(TemplateView):
    template_name = "main/detail.html"

