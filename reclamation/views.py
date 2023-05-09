from django.urls import reverse_lazy
from django.views.generic import *
from django.conf import settings
from core.models import ItemCategory, ItemQuestionResponse
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, get_object_or_404
from .forms import ReclamationForm


class ReclamationListView(ListView):
    model = Reclamation
    template_name = "home/pages/reclamation_list.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            return redirect('item_list')
        return super().dispatch(request, *args, **kwargs)


class ReclamationListViewForUser(ListView):
    model = Reclamation
    template_name = "home/pages/reclamation_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class ReclamationCreateView(CreateView):
    model = Reclamation
    form_class = ReclamationForm
    success_url = reverse_lazy('item_list')
    template_name = "home/pages/add_reclamation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_type = self.kwargs.get('item_type')
        category = get_object_or_404(ItemCategory, name=item_type)
        item_questions = category.questions.filter(is_for_reclamation=True)
        context['item_type'] = item_type
        context['item_questions'] = item_questions
        return context

    def form_valid(self, form):
        reclamation = form.save(commit=False)
        reclamation.save()
        category = form.cleaned_data.get('categories')
        category_questions = category.questions.all()
        for question in category_questions:
            answer = form.cleaned_data.get(question.question)
            ItemQuestionResponse.objects.create(category=category, question=question, answer=answer,
                                                reclamation=reclamation)
        return redirect('item-detail', pk=reclamation.pk)


class ReclamationUpdateView(UpdateView):
    model = Reclamation
    form_class = ReclamationForm
    success_url = reverse_lazy('item_list')


class ReclamationDeleteView(DeleteView):
    model = Reclamation
    success_url = reverse_lazy('item_list')


class ReclamationDetailView(DetailView):
    model = Reclamation
    template_name = "home/pages/detail_reclamation.html"

    def dispatch(self, request, *args, **kwargs):
        print("test_dispatch")
        return super().dispatch(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['test'] = 'test'
    #     other_item_information = ItemQuestionResponse.objects.filter(reclamation=self.object)
    #     item_question_tag_for_name = other_item_information.filter(question__tag__name="Name").first()
    #     item_name = item_question_tag_for_name
    #     context['other_item_information'] = other_item_information
    #     context['item_name'] = item_name
    #     context['mapbox_access_token'] = settings.MAPBOX_ACCESS_TOKEN
    #     context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
    #     return context


class ReclamationListViewAccepted(ListView):
    model = Reclamation
    template_name = "home/pages/reclamation_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status="Accepted")
        return queryset


class ReclamationListViewRejected(ListView):
    model = Reclamation
    template_name = "home/pages/reclamation_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status="Rejected")
        return queryset


class ReclamationListViewPending(ListView):
    model = Reclamation
    template_name = "home/pages/reclamation_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(status="Pending")
        return queryset
