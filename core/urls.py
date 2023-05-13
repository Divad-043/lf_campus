from django.urls import path, include
from .views import *

app_name = "core"

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    # path('item/detail', views.DetailItemView.as_view(), name="detail"),
    # path('item/add/', )
    path('item/list', ItemListView.as_view(), name='item_list'),
    path('item/create/', ItemCreateView.as_view(), name='item_create'),
    path('item/<int:pk>/update/', ItemUpdateView.as_view(), name='item_update'),
    path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item_delete'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item_detail'),

]