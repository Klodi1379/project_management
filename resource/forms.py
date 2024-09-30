from django import forms
from .models import ResourceCategory, Resource, ResourceAllocation, MaintenanceLog

class ResourceCategoryForm(forms.ModelForm):
    class Meta:
        model = ResourceCategory
        fields = ['name', 'description']

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'category', 'description', 'quantity', 'acquisition_date', 'cost', 'status']
        widgets = {
            'acquisition_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ResourceAllocationForm(forms.ModelForm):
    class Meta:
        model = ResourceAllocation
        fields = ['resource', 'project', 'user', 'start_date', 'end_date', 'quantity_allocated', 'notes']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class MaintenanceLogForm(forms.ModelForm):
    class Meta:
        model = MaintenanceLog
        fields = ['resource', 'maintenance_date', 'performed_by', 'description', 'cost']
        widgets = {
            'maintenance_date': forms.DateInput(attrs={'type': 'date'}),
        }