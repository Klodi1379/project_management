from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    
    path('', views.ProjectListView.as_view(), name='list'),
    path('dashboard/', views.ProjectDashboardView.as_view(), name='dashboard'),
    path('create/', views.ProjectCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.ProjectUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='delete'),
    path('<int:project_id>/task/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('task/<int:task_id>/add_comment/', views.add_comment, name='add_comment'),
    path('report/', views.ProjectReportView.as_view(), name='report'),
    
    path('notifications/', views.NotificationListView.as_view(), name='notifications'),
]