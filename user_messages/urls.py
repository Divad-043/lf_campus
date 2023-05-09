from django.urls import path
from . import views

app_name = "user_messages"

urlpatterns = [
    path("all/", views.IndexMessageView.as_view(), name="index"),
    path("list/", views.MessageListView.as_view(), name="list"),
    path("create/", views.MessageCreateView.as_view(), name="create"),
    path("detail/<int:pk>/", views.MessageDetailView.as_view(), name="detail"),
    path("delete/<int:pk>/", views.MessageDeleteView.as_view(), name="delete"),


]
