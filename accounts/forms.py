from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import CustomUser, UserProfile, Team
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'role', 'date_of_birth', 'phone_number')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role', 'bio', 'profile_picture', 'date_of_birth', 'phone_number', 'address', 'linkedin_profile', 'github_profile')

class UserProfileForm(forms.ModelForm):
    skills = forms.CharField(widget=forms.TextInput(attrs={'data-role': 'tagsinput'}), required=False)
    certifications = forms.CharField(widget=forms.TextInput(attrs={'data-role': 'tagsinput'}), required=False)

    class Meta:
        model = UserProfile
        fields = ('department', 'skills', 'certifications', 'years_of_experience', 'preferred_working_hours')

    def clean_skills(self):
        return self.cleaned_data['skills'].split(',')

    def clean_certifications(self):
        return self.cleaned_data['certifications'].split(',')

class AdvancedLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()

class SetNewPasswordForm(PasswordChangeForm):
    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError("The two password fields didn't match.")
        return password2

class TeamCreationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'leader', 'members', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['leader'].queryset = CustomUser.objects.filter(role__in=['manager', 'team_lead'])
        self.fields['members'].queryset = CustomUser.objects.all()
        self.fields['members'].widget = forms.CheckboxSelectMultiple()



class NotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email_notifications', 'push_notifications', 'notification_frequency']
        widgets = {
            'notification_frequency': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email_notifications'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['push_notifications'].widget.attrs.update({'class': 'form-check-input'})