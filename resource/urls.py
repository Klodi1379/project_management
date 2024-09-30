from django.urls import path
from . import views

app_name = 'resource'

urlpatterns = [
    # Resource Category URLs
    path('categories/', views.ResourceCategoryListView.as_view(), name='category_list'),
    path('category/create/', views.ResourceCategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/update/', views.ResourceCategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', views.ResourceCategoryDeleteView.as_view(), name='category_delete'),

    # Resource URLs
    path('', views.ResourceListView.as_view(), name='resource_list'),
    path('<int:pk>/', views.ResourceDetailView.as_view(), name='resource_detail'),
    path('create/', views.ResourceCreateView.as_view(), name='resource_create'),
    path('<int:pk>/update/', views.ResourceUpdateView.as_view(), name='resource_update'),
    path('<int:pk>/delete/', views.ResourceDeleteView.as_view(), name='resource_delete'),

    # Resource Allocation URLs
    path('allocations/', views.ResourceAllocationListView.as_view(), name='allocation_list'),
    path('allocation/create/', views.ResourceAllocationCreateView.as_view(), name='allocation_create'),
    path('allocation/<int:pk>/update/', views.ResourceAllocationUpdateView.as_view(), name='allocation_update'),
    path('allocation/<int:pk>/delete/', views.ResourceAllocationDeleteView.as_view(), name='allocation_delete'),

    # Maintenance Log URLs
    path('maintenance-logs/', views.MaintenanceLogListView.as_view(), name='maintenance_log_list'),
    path('maintenance-log/create/', views.MaintenanceLogCreateView.as_view(), name='maintenance_log_create'),
    path('maintenance-log/<int:pk>/update/', views.MaintenanceLogUpdateView.as_view(), name='maintenance_log_update'),
    path('maintenance-log/<int:pk>/delete/', views.MaintenanceLogDeleteView.as_view(), name='maintenance_log_delete'),
]