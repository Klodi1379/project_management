from django.urls import path
from . import views

app_name = 'reporting'

urlpatterns = [
    path('', views.ReportListView.as_view(), name='report_list'),
    path('create/', views.ReportCreateView.as_view(), name='report_create'),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('<int:pk>/update/', views.ReportUpdateView.as_view(), name='report_update'),
    path('<int:pk>/delete/', views.ReportDeleteView.as_view(), name='report_delete'),
    path('<int:pk>/export/', views.export_report_csv, name='report_export_csv'),
    path('<int:pk>/chart/', views.generate_report_chart, name='report_chart'),
    path('schedule/create/', views.ReportScheduleCreateView.as_view(), name='report_schedule_create'),
    path('schedule/<int:pk>/update/', views.ReportScheduleUpdateView.as_view(), name='report_schedule_update'),
    path('schedule/<int:pk>/delete/', views.ReportScheduleDeleteView.as_view(), name='report_schedule_delete'),
]