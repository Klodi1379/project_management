from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import ResourceCategory, Resource, ResourceAllocation, MaintenanceLog
from .forms import ResourceCategoryForm, ResourceForm, ResourceAllocationForm, MaintenanceLogForm

# ResourceCategory Views
class ResourceCategoryListView(LoginRequiredMixin, ListView):
    model = ResourceCategory
    template_name = 'resource/category_list.html'
    context_object_name = 'categories'

class ResourceCategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ResourceCategory
    form_class = ResourceCategoryForm
    template_name = 'resource/category_form.html'
    success_url = reverse_lazy('resources:category_list')
    permission_required = 'resources.add_resourcecategory'

    def form_valid(self, form):
        messages.success(self.request, 'Resource category created successfully.')
        return super().form_valid(form)

class ResourceCategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ResourceCategory
    form_class = ResourceCategoryForm
    template_name = 'resource/category_form.html'
    success_url = reverse_lazy('resources:category_list')
    permission_required = 'resources.change_resourcecategory'

    def form_valid(self, form):
        messages.success(self.request, 'Resource category updated successfully.')
        return super().form_valid(form)

class ResourceCategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ResourceCategory
    template_name = 'resource/category_confirm_delete.html'
    success_url = reverse_lazy('resources:category_list')
    permission_required = 'resources.delete_resourcecategory'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Resource category deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Resource Views
class ResourceListView(LoginRequiredMixin, ListView):
    model = Resource
    template_name = 'resource/resource_list.html'
    context_object_name = 'resources'

class ResourceDetailView(LoginRequiredMixin, DetailView):
    model = Resource
    template_name = 'resource/resource_detail.html'
    context_object_name = 'resource'

class ResourceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Resource
    form_class = ResourceForm
    template_name = 'resource/resource_form.html'
    success_url = reverse_lazy('resources:resource_list')
    permission_required = 'resources.add_resource'

    def form_valid(self, form):
        messages.success(self.request, 'Resource created successfully.')
        return super().form_valid(form)

class ResourceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Resource
    form_class = ResourceForm
    template_name = 'resource/resource_form.html'
    success_url = reverse_lazy('resources:resource_list')
    permission_required = 'resources.change_resource'

    def form_valid(self, form):
        messages.success(self.request, 'Resource updated successfully.')
        return super().form_valid(form)

class ResourceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Resource
    template_name = 'resource/resource_confirm_delete.html'
    success_url = reverse_lazy('resources:resource_list')
    permission_required = 'resources.delete_resource'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Resource deleted successfully.')
        return super().delete(request, *args, **kwargs)

# ResourceAllocation Views
class ResourceAllocationListView(LoginRequiredMixin, ListView):
    model = ResourceAllocation
    template_name = 'resource/allocation_list.html'
    context_object_name = 'allocations'

class ResourceAllocationCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ResourceAllocation
    form_class = ResourceAllocationForm
    template_name = 'resource/allocation_form.html'
    success_url = reverse_lazy('resources:allocation_list')
    permission_required = 'resources.add_resourceallocation'

    def form_valid(self, form):
        messages.success(self.request, 'Resource allocation created successfully.')
        return super().form_valid(form)

class ResourceAllocationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ResourceAllocation
    form_class = ResourceAllocationForm
    template_name = 'resource/allocation_form.html'
    success_url = reverse_lazy('resources:allocation_list')
    permission_required = 'resources.change_resourceallocation'

    def form_valid(self, form):
        messages.success(self.request, 'Resource allocation updated successfully.')
        return super().form_valid(form)

class ResourceAllocationDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ResourceAllocation
    template_name = 'resource/allocation_confirm_delete.html'
    success_url = reverse_lazy('resources:allocation_list')
    permission_required = 'resources.delete_resourceallocation'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Resource allocation deleted successfully.')
        return super().delete(request, *args, **kwargs)

# MaintenanceLog Views
class MaintenanceLogListView(LoginRequiredMixin, ListView):
    model = MaintenanceLog
    template_name = 'resource/maintenance_log_list.html'
    context_object_name = 'maintenance_logs'

class MaintenanceLogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = MaintenanceLog
    form_class = MaintenanceLogForm
    template_name = 'resource/maintenance_log_form.html'
    success_url = reverse_lazy('resources:maintenance_log_list')
    permission_required = 'resources.add_maintenancelog'

    def form_valid(self, form):
        messages.success(self.request, 'Maintenance log created successfully.')
        return super().form_valid(form)

class MaintenanceLogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MaintenanceLog
    form_class = MaintenanceLogForm
    template_name = 'resource/maintenance_log_form.html'
    success_url = reverse_lazy('resources:maintenance_log_list')
    permission_required = 'resources.change_maintenancelog'

    def form_valid(self, form):
        messages.success(self.request, 'Maintenance log updated successfully.')
        return super().form_valid(form)

class MaintenanceLogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MaintenanceLog
    template_name = 'resource/maintenance_log_confirm_delete.html'
    success_url = reverse_lazy('resources:maintenance_log_list')
    permission_required = 'resources.delete_maintenancelog'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Maintenance log deleted successfully.')
        return super().delete(request, *args, **kwargs)