from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Client, Contact, ClientInteraction, ClientDocument
from .forms import ClientForm, ContactForm, ClientInteractionForm, ClientDocumentForm, ClientSearchForm



class ClientListView(ListView):
    model = Client
    template_name = 'crm/client_list.html'
    context_object_name = 'clients'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        industry = self.request.GET.get('industry')
        sort = self.request.GET.get('sort', 'name')

        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(industry__icontains=search))
        if industry:
            queryset = queryset.filter(industry=industry)
        
        return queryset.order_by(sort)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['industries'] = Client.objects.values_list('industry', flat=True).distinct()
        return context

class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'crm/client_detail.html'
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = self.object.contacts.all()
        context['interactions'] = self.object.interactions.order_by('-date')[:5]
        context['documents'] = self.object.documents.order_by('-uploaded_at')[:5]
        context['projects'] = self.object.projects.all()
        return context

class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'crm/client_form.html'
    success_url = reverse_lazy('crm:client_list')
    permission_required = 'crm.add_client'

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to add clients.")
        return redirect('crm:client_list')

class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'crm/client_form.html'
    success_url = reverse_lazy('crm:client_list')
    permission_required = 'crm.change_client'

    def form_valid(self, form):
        messages.success(self.request, 'Client updated successfully.')
        return super().form_valid(form)

class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    template_name = 'crm/client_confirm_delete.html'
    success_url = reverse_lazy('crm:client_list')
    permission_required = 'crm.delete_client'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Client deleted successfully.')
        return super().delete(request, *args, **kwargs)

class ContactCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'crm/contact_form.html'
    permission_required = 'crm.add_contact'

    def get_success_url(self):
        return reverse_lazy('crm:client_detail', kwargs={'pk': self.object.client.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Contact created successfully.')
        return super().form_valid(form)

class ContactUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'crm/contact_form.html'
    permission_required = 'crm.change_contact'

    def get_success_url(self):
        return reverse_lazy('crm:client_detail', kwargs={'pk': self.object.client.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Contact updated successfully.')
        return super().form_valid(form)

class ContactDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Contact
    template_name = 'crm/contact_confirm_delete.html'
    permission_required = 'crm.delete_contact'

    def get_success_url(self):
        return reverse_lazy('crm:client_detail', kwargs={'pk': self.object.client.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Contact deleted successfully.')
        return super().delete(request, *args, **kwargs)

class ClientInteractionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ClientInteraction
    form_class = ClientInteractionForm
    template_name = 'crm/interaction_form.html'
    permission_required = 'crm.add_clientinteraction'

    def get_success_url(self):
        return reverse_lazy('crm:client_detail', kwargs={'pk': self.object.client.pk})

    def form_valid(self, form):
        form.instance.conducted_by = self.request.user
        messages.success(self.request, 'Interaction recorded successfully.')
        return super().form_valid(form)

class ClientInteractionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ClientInteraction
    form_class = ClientInteractionForm
    template_name = 'crm/interaction_form.html'
    permission_required = 'crm.change_clientinteraction'

    def get_success_url(self):
        return reverse_lazy('crm:client_detail', kwargs={'pk': self.object.client.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Interaction updated successfully.')
        return super().form_valid(form)

class ClientDocumentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ClientDocument
    form_class = ClientDocumentForm
    template_name = 'crm/document_form.html'
    permission_required = 'crm.add_clientdocument'

    def get_success_url(self):
        return reverse_lazy('crm:client_detail', kwargs={'pk': self.object.client.pk})

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, 'Document uploaded successfully.')
        return super().form_valid(form)

class ClientDocumentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ClientDocument
    template_name = 'crm/document_confirm_delete.html'
    permission_required = 'crm.delete_clientdocument'

    def get_success_url(self):
        return reverse_lazy('crm:client_detail', kwargs={'pk': self.object.client.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Document deleted successfully.')
        return super().delete(request, *args, **kwargs)