from django.urls import path, include
from . import views

app_name = "core"

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('item/detail', views.DetailItemView.as_view(), name="detail")
]