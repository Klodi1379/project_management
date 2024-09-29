from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('reset-password/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('team/create/', views.team_create, name='team_create'),
    path('team/<int:team_id>/', views.team_detail, name='team_detail'),
    path('notification-settings/', views.notification_settings, name='notification_settings'),
    path('mark-notification-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('user-search/', views.user_search, name='user_search'),
    path('user-management/', views.user_management, name='user_management'),
    path('deactivate-user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('team-list/', views.team_list, name='team_list'),
    path('team-update/<int:team_id>/', views.team_update, name='team_update'),
    path('user-activity/', views.user_activity, name='user_activity'),
    path('export-users-csv/', views.export_users_csv, name='export_users_csv'),
    path('update-profile-picture/', views.update_profile_picture, name='update_profile_picture'),
    path('api-key-management/', views.api_key_management, name='api_key_management'),
    path('account-settings/', views.account_settings, name='account_settings'),
    path('oauth-login/<str:provider>/', views.oauth_login, name='oauth_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]