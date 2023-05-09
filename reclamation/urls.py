from django.urls import path
from .views import *

app_name = "reclamation"

urlpatterns = [
    path('item/<uuid:pk>/reclamation/', ReclamationCreateView.as_view(), name='item_reclamation'),
    path('reclamation/update/', ReclamationUpdateView.as_view(), name='item_reclamation_update'),
    path('reclamation/delete/', ReclamationDeleteView.as_view(), name='item_reclamation_delete'),
    path('reclamation/detail/', ReclamationDetailView.as_view(), name='item_reclamation_detail'),
    path('reclamation/list/', ReclamationListViewForUser.as_view(), name='item_reclamation_list'),
    path('reclamation/list/all/', ReclamationListView.as_view(), name='item_reclamation_list_all'),
    path('reclamation/list/accepted/', ReclamationListViewAccepted.as_view(), name='item_reclamation_list_accepted'),
    path('reclamation/list/rejected/', ReclamationListViewRejected.as_view(), name='item_reclamation_list_rejected'),
    path('reclamation/list/pending/', ReclamationListViewPending.as_view(), name='item_reclamation_list_pending'),
]