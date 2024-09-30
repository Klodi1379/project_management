from django import forms
from .models import Client, Contact, ClientInteraction, ClientDocument

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'industry', 'website', 'description', 'address']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['client', 'name', 'position', 'email', 'phone', 'is_primary', 'notes']

class ClientInteractionForm(forms.ModelForm):
    class Meta:
        model = ClientInteraction
        fields = ['client', 'interaction_type', 'date', 'summary', 'conducted_by', 'contact', 'related_project']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ClientDocumentForm(forms.ModelForm):
    class Meta:
        model = ClientDocument
        fields = ['client', 'title', 'document']

class ClientSearchForm(forms.Form):
    search = forms.CharField(required=False, label='Search Clients')
    industry = forms.CharField(required=False)
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))