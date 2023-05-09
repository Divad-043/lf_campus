from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import *
from .models import *
from django.db.models import Q


class IndexMessageView(ListView):
    model = UserMessage
    template_name = "dashboard/pages/chat.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(Q(sender=user) | Q(receiver=user))
        return queryset


class SendMessageView(CreateView):
    model = UserMessage
    fields = ['receiver', 'content']
    success_url = reverse_lazy('index_message')

    def form_valid(self, form):
        message = form.save(commit=False)
        message.sender = self.request.user
        message.save()
        return super().form_valid(form)


class MessageListView(ListView):
    model = UserMessage
    template_name = "dashboard/pages/chat.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(Q(sender=user) | Q(receiver=user))
        return queryset


class MessageCreateView(CreateView):
    model = UserMessage
    fields = ['receiver', 'content']
    success_url = reverse_lazy('index_message')

    def form_valid(self, form):
        message = form.save(commit=False)
        message.sender = self.request.user
        message.save()
        return super().form_valid(form)


class MessageDetailView(DetailView):
    model = UserMessage
    template_name = "dashboard/pages/chat.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(Q(sender=user) | Q(receiver=user))
        return queryset


class MessageDeleteView(DeleteView):
    model = UserMessage
    success_url = reverse_lazy('index_message')

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(Q(sender=user) | Q(receiver=user))
        return queryset


class IndexDiscussionView(ListView):
    model = Discussion
    template_name = "dashboard/pages/discussion.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(Q(user1=user) | Q(user2=user))
        return queryset


class DiscussionListView(ListView):
    model = Discussion
    template_name = "dashboard/pages/discussion.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(Q(user1=user) | Q(user2=user))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        discussions = self.get_queryset()
        context['discussions'] = discussions
        return context


class DiscussionDetailView(DetailView):
    model = Discussion
    template_name = "dashboard/pages/discussion_detail.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(Q(user1=user) | Q(user2=user))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        discussions = self.get_queryset()
        context['discussions'] = discussions
        return context
