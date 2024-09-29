from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from django.http import HttpResponse
from django.views import View
from .models import Notification, Project, Task, Comment
from .forms import ProjectForm, TaskForm, CommentForm
import csv


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10

    def get_queryset(self):
        queryset = Project.objects.filter(team_members=self.request.user)
        
        # Search
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(client__icontains=search_query)
            )
        
        # Filtering
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Sorting
        sort_by = self.request.GET.get('sort_by', 'name')
        if sort_by == 'deadline':
            queryset = queryset.order_by('end_date')
        elif sort_by == 'priority':
            queryset = queryset.order_by('-priority')
        else:
            queryset = queryset.order_by('name')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['current_priority'] = self.request.GET.get('priority', '')
        context['current_sort'] = self.request.GET.get('sort_by', 'name')
        return context

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.object.tasks.all()
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:list')

    def form_valid(self, form):
        form.instance.manager = self.request.user
        messages.success(self.request, 'Project created successfully.')
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:list')

    def test_func(self):
        return self.request.user == self.get_object().manager

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.has_changed():
            for member in self.object.team_members.all():
                Notification.objects.create(
                    user=member,
                    notification_type='status_change',
                    project=self.object,
                    message=f"Project '{self.object.name}' has been updated."
                )
        messages.success(self.request, 'Project updated successfully.')
        return response

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('projects:list')

    def test_func(self):
        return self.request.user == self.get_object().manager

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Project deleted successfully.')
        return super().delete(request, *args, **kwargs)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:list')

    def test_func(self):
        return self.request.user == self.get_object().manager

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.has_changed():
            for member in self.object.team_members.all():
                Notification.objects.create(
                    user=member,
                    notification_type='status_change',
                    project=self.object,
                    message=f"Project '{self.object.name}' has been updated."
                )
        messages.success(self.request, 'Project updated successfully.')
        return response
from .mixins import NotificationContextMixin    
    
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Project, Task, Comment
from .forms import TaskForm, CommentForm
from projects.mixins import NotificationContextMixin

class TaskCreateView(NotificationContextMixin, LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'projects/task_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.project = self.project
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Task created successfully.')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context

    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={'pk': self.project.pk})

class TaskUpdateView(NotificationContextMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'projects/task_form.html'

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.project.manager or self.request.user == task.assigned_to

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Task updated successfully.')
        return response

    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.project.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.object.project
        return context
class TaskDeleteView(NotificationContextMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'projects/task_confirm_delete.html'

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.project.manager

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Task deleted successfully.')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.project.id})

class TaskDetailView(NotificationContextMixin, DetailView):
    model = Task
    template_name = 'projects/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class TaskListView(NotificationContextMixin, ListView):
    model = Task
    template_name = 'projects/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        return Task.objects.filter(project__team_members=self.request.user).order_by('-created_at')

def add_comment(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('projects:task_detail', pk=task.id)
    return redirect('projects:task_detail', pk=task.id)




from django.db.models import Count, Q
from django.utils import timezone

class ProjectDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Projects statistics
        context['total_projects'] = Project.objects.filter(team_members=user).count()
        context['active_projects'] = Project.objects.filter(team_members=user, status='active').count()
        context['completed_projects'] = Project.objects.filter(team_members=user, status='completed').count()

        # Tasks statistics
        context['total_tasks'] = Task.objects.filter(project__team_members=user).count()
        context['tasks_completed'] = Task.objects.filter(project__team_members=user, status='completed').count()
        context['tasks_in_progress'] = Task.objects.filter(project__team_members=user, status='in_progress').count()
        context['overdue_tasks'] = Task.objects.filter(
            project__team_members=user,
            due_date__lt=timezone.now().date(),
            status__in=['not_started', 'in_progress']
        ).count()

        # Recent projects
        context['recent_projects'] = Project.objects.filter(team_members=user).order_by('-created_at')[:5]

        # Upcoming deadlines
        context['upcoming_deadlines'] = Task.objects.filter(
            project__team_members=user,
            due_date__gte=timezone.now().date(),
            status__in=['not_started', 'in_progress']
        ).order_by('due_date')[:5]

        return context
    
    
    
from django.http import HttpResponse
import csv

class ProjectReportView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="project_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Project Name', 'Status', 'Start Date', 'End Date', 'Completion %', 'Tasks Count'])

        projects = Project.objects.filter(team_members=request.user)
        for project in projects:
            writer.writerow([
                project.name,
                project.get_status_display(),
                project.start_date,
                project.end_date,
                project.get_completion_percentage(),
                project.tasks.count()
            ])

        return response
    
    
    
    
class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'projects/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')    
    

    
    
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['recent_projects'] = Project.objects.filter(team_members=user).order_by('-created_at')[:5]
        context['upcoming_tasks'] = Task.objects.filter(assigned_to=user, status__in=['not_started', 'in_progress']).order_by('due_date')[:5]
        context['unread_notifications'] = user.project_notifications.filter(is_read=False).count()
        return context    