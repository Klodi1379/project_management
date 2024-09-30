from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_POST
from .forms import (
    CustomUserCreationForm, CustomUserChangeForm, UserProfileForm, 
    AdvancedLoginForm, PasswordResetRequestForm, SetNewPasswordForm,
    TeamCreationForm, NotificationSettingsForm
)
from .models import CustomUser, UserProfile, Team, Notification, UserActivity
import logging

logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            UserActivity.objects.create(user=user, activity_type='registration', description='User registered')
            messages.success(request, 'Registration successful.')
            return redirect('accounts:profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AdvancedLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                UserActivity.objects.create(user=user, activity_type='login', description='User logged in')
                messages.success(request, 'Login successful.')
                return redirect('accounts:profile')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AdvancedLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def user_logout(request):
    UserActivity.objects.create(user=request.user, activity_type='logout', description='User logged out')
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            UserActivity.objects.create(user=request.user, activity_type='profile_update', description='User updated profile')
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('accounts:profile')
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.filter(email=email).first()
            if user:
                token = get_random_string(length=32)
                user.password_reset_token = token
                user.save()
                reset_url = request.build_absolute_uri(f'/accounts/reset-password/{token}/')
                send_mail(
                    'Password Reset Request',
                    f'Click here to reset your password: {reset_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Password reset email sent.')
            else:
                messages.error(request, 'No user found with that email address.')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'accounts/password_reset_request.html', {'form': form})

def password_reset_confirm(request, token):
    user = get_object_or_404(CustomUser, password_reset_token=token)
    if request.method == 'POST':
        form = SetNewPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            user.password_reset_token = None
            user.save()
            UserActivity.objects.create(user=user, activity_type='password_reset', description='User reset password')
            messages.success(request, 'Your password has been reset successfully.')
            return redirect('accounts:login')
    else:
        form = SetNewPasswordForm(user)
    return render(request, 'accounts/password_reset_confirm.html', {'form': form})

@login_required
def team_create(request):
    if request.method == 'POST':
        form = TeamCreationForm(request.POST)
        if form.is_valid():
            team = form.save()
            UserActivity.objects.create(user=request.user, activity_type='team_created', description=f'User created team: {team.name}')
            messages.success(request, 'Team created successfully.')
            return redirect('accounts:team_detail', team_id=team.id)
    else:
        form = TeamCreationForm()
    return render(request, 'accounts/team_form.html', {'form': form})

@login_required
def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    return render(request, 'accounts/team_detail.html', {'team': team})

@login_required
def notification_settings(request):
    if request.method == 'POST':
        form = NotificationSettingsForm(request.POST)
        if form.is_valid():
            # Save notification settings to user profile
            profile = request.user.profile
            profile.email_notifications = form.cleaned_data['email_notifications']
            profile.push_notifications = form.cleaned_data['push_notifications']
            profile.notification_frequency = form.cleaned_data['notification_frequency']
            profile.save()
            messages.success(request, 'Notification settings updated successfully.')
            return redirect('accounts:profile')
    else:
        profile = request.user.profile
        initial_data = {
            'email_notifications': profile.email_notifications,
            'push_notifications': profile.push_notifications,
            'notification_frequency': profile.notification_frequency
        }
        form = NotificationSettingsForm(initial=initial_data)
    return render(request, 'accounts/notification_settings.html', {'form': form})

@login_required
@require_POST
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    
    
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import CustomUser, Team, UserActivity
import csv
from django.http import HttpResponse

@login_required
def user_search(request):
    query = request.GET.get('q')
    if query:
        users = CustomUser.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    else:
        users = CustomUser.objects.all()
    
    paginator = Paginator(users, 20)  # Show 20 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'accounts/user_search.html', {'page_obj': page_obj, 'query': query})

@login_required
@user_passes_test(lambda u: u.role in ['admin', 'manager'])
def user_management(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'accounts/user_management.html', {'users': users})

@login_required
@user_passes_test(lambda u: u.role in ['admin', 'manager'])
def deactivate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = False
    user.save()
    UserActivity.objects.create(user=request.user, activity_type='user_deactivation', description=f'Deactivated user: {user.username}')
    messages.success(request, f'User {user.username} has been deactivated.')
    return redirect('accounts:user_management')

@login_required
def team_list(request):
    teams = Team.objects.all()
    return render(request, 'accounts/team_list.html', {'teams': teams})

@login_required
@user_passes_test(lambda u: u.role in ['admin', 'manager', 'team_lead'])
def team_update(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == 'POST':
        form = TeamCreationForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            UserActivity.objects.create(user=request.user, activity_type='team_update', description=f'Updated team: {team.name}')
            messages.success(request, 'Team updated successfully.')
            return redirect('accounts:team_detail', team_id=team.id)
    else:
        form = TeamCreationForm(instance=team)
    return render(request, 'accounts/team_update.html', {'form': form, 'team': team})

@login_required
def user_activity(request):
    activities = UserActivity.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'accounts/user_activity.html', {'activities': activities})

@login_required
@user_passes_test(lambda u: u.role == 'admin')
def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'Email', 'Role', 'Date Joined', 'Last Login'])

    users = CustomUser.objects.all().values_list('username', 'email', 'role', 'date_joined', 'last_login')
    for user in users:
        writer.writerow(user)

    return response

@login_required
def update_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        request.user.profile_picture = request.FILES['profile_picture']
        request.user.save()
        UserActivity.objects.create(user=request.user, activity_type='profile_picture_update', description='Updated profile picture')
        return JsonResponse({'success': True, 'message': 'Profile picture updated successfully.'})
    return JsonResponse({'success': False, 'message': 'Failed to update profile picture.'})

@login_required
def api_key_management(request):
    if request.method == 'POST':
        # Generate new API key
        new_key = get_random_string(length=40)
        request.user.api_key = new_key
        request.user.save()
        UserActivity.objects.create(user=request.user, activity_type='api_key_generation', description='Generated new API key')
        messages.success(request, 'New API key generated successfully.')
    return render(request, 'accounts/api_key_management.html')

@login_required
def account_settings(request):
    if request.method == 'POST':
        # Handle account settings updates
        two_factor_auth = request.POST.get('two_factor_auth') == 'on'
        request.user.profile.two_factor_auth = two_factor_auth
        request.user.profile.save()
        UserActivity.objects.create(user=request.user, activity_type='account_settings_update', description='Updated account settings')
        messages.success(request, 'Account settings updated successfully.')
    return render(request, 'accounts/account_settings.html')

def oauth_login(request, provider):
    # Implement OAuth login logic here
    # This is a placeholder and would need to be implemented with a proper OAuth library
    pass

@login_required
def dashboard(request):
    user_teams = request.user.teams.all()
    recent_activities = UserActivity.objects.filter(user=request.user).order_by('-timestamp')[:5]
    return render(request, 'accounts/dashboard.html', {
        'user_teams': user_teams,
        'recent_activities': recent_activities
    })    
    
    
    
    
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm, NotificationSettingsForm
from .models import NotificationSettings

@login_required
def notification_settings(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = NotificationSettingsForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notification settings updated successfully.')
            return redirect('accounts:profile')
    else:
        form = NotificationSettingsForm(instance=user_profile)
    
    return render(request, 'accounts/notification_settings.html', {'form': form})
@login_required
def update_notification_settings(request):
    if request.method == 'POST':
        notification_settings, created = NotificationSettings.objects.get_or_create(user=request.user)
        form = NotificationSettingsForm(request.POST, instance=notification_settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notification settings updated successfully.')
        else:
            messages.error(request, 'There was an error updating your notification settings.')
    return redirect('accounts:account_settings')