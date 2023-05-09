from django.urls import path, include
from .views import *

app_name = "core"

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    # path("test/", test, name="test"),
    # path('item/detail', views.DetailItemView.as_view(), name="detail"),
    # path('item/add/', )
    path('item/list', ItemListView.as_view(), name='item_list'),
    path('item/create/<str:item_type>/', ItemCreateView.as_view(), name='item_create'),
    path('item/<int:pk>/update/', ItemUpdateView.as_view(), name='item_update'),
    path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item_delete'),
    path('item/<uuid:pk>/', ItemDetailView.as_view(), name='item_detail'),
    path('item/search/', ItemSearchView.as_view(), name='item_search'),
    path('item/reclamation/', include('reclamation.urls', namespace='reclamation')),
    path('item/list/<slug:item_type>/', ItemExploreByCategoryView.as_view(), name="explore_by_category"),
    path('item/university/<slug:university_slug>/', ExploreByUniversityView.as_view(), name="explore_by_university")
]
