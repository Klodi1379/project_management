from django import forms
from .models import Report, ReportSchedule
from projects.models import Project
from resource.models import Resource
from crm.models import Client

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'report_type', 'description', 'project', 'resource', 'client', 'date_range_start', 'date_range_end']
        widgets = {
            'date_range_start': forms.DateInput(attrs={'type': 'date'}),
            'date_range_end': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.all()
        self.fields['resource'].queryset = Resource.objects.all()
        self.fields['client'].queryset = Client.objects.all()

class ReportScheduleForm(forms.ModelForm):
    class Meta:
        model = ReportSchedule
        fields = ['report', 'frequency', 'recipients', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipients'].widget = forms.CheckboxSelectMultiple()
        self.fields['recipients'].queryset = self.fields['recipients'].queryset.order_by('username')

class ReportFilterForm(forms.Form):
    report_type = forms.ChoiceField(choices=[('', 'All')] + Report.REPORT_TYPES, required=False)
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    project = forms.ModelChoiceField(queryset=Project.objects.all(), required=False, empty_label="All Projects")
    client = forms.ModelChoiceField(queryset=Client.objects.all(), required=False, empty_label="All Clients")