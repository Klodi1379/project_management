from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    # Client URLs
    path('', views.ClientListView.as_view(), name='client_list'),
    path('create/', views.ClientCreateView.as_view(), name='client_create'),
    path('<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('<int:pk>/update/', views.ClientUpdateView.as_view(), name='client_update'),
    path('<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),

    # Contact URLs
    path('contact/create/', views.ContactCreateView.as_view(), name='contact_create'),
    path('contact/<int:pk>/update/', views.ContactUpdateView.as_view(), name='contact_update'),
    path('contact/<int:pk>/delete/', views.ContactDeleteView.as_view(), name='contact_delete'),

    # Interaction URLs
    path('interaction/create/', views.ClientInteractionCreateView.as_view(), name='interaction_create'),
    path('interaction/<int:pk>/update/', views.ClientInteractionUpdateView.as_view(), name='interaction_update'),

    # Document URLs
    path('document/create/', views.ClientDocumentCreateView.as_view(), name='document_create'),
    path('document/<int:pk>/delete/', views.ClientDocumentDeleteView.as_view(), name='document_delete'),
]