from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from .models import Report, ReportSchedule
from .forms import ReportForm, ReportScheduleForm, ReportFilterForm
from projects.models import Project, Task
from resource.models import Resource, ResourceAllocation
from crm.models import Client, ClientInteraction
import csv
import io
import matplotlib.pyplot as plt
import seaborn as sns

class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'reporting/report_list.html'
    context_object_name = 'reports'
    paginate_by = 10

    def get_queryset(self):
        queryset = Report.objects.all()
        form = ReportFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['report_type']:
                queryset = queryset.filter(report_type=form.cleaned_data['report_type'])
            if form.cleaned_data['date_from']:
                queryset = queryset.filter(created_at__gte=form.cleaned_data['date_from'])
            if form.cleaned_data['date_to']:
                queryset = queryset.filter(created_at__lte=form.cleaned_data['date_to'])
            if form.cleaned_data['project']:
                queryset = queryset.filter(project=form.cleaned_data['project'])
            if form.cleaned_data['client']:
                queryset = queryset.filter(client=form.cleaned_data['client'])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ReportFilterForm(self.request.GET)
        return context

class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'reporting/report_detail.html'
    context_object_name = 'report'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report = self.object
        context['report_data'] = self.generate_report_data(report)
        return context

    def generate_report_data(self, report):
        if report.report_type == 'project_progress':
            return self.generate_project_progress_report(report)
        elif report.report_type == 'resource_utilization':
            return self.generate_resource_utilization_report(report)
        elif report.report_type == 'team_performance':
            return self.generate_team_performance_report(report)
        elif report.report_type == 'financial_summary':
            return self.generate_financial_summary_report(report)
        elif report.report_type == 'client_overview':
            return self.generate_client_overview_report(report)
        else:
            return None

    def generate_project_progress_report(self, report):
        project = report.project
        if not project:
            return None

        total_tasks = Task.objects.filter(project=project).count()
        completed_tasks = Task.objects.filter(project=project, status='completed').count()
        progress_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

        return {
            'project_name': project.name,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'progress_percentage': round(progress_percentage, 2),
            'start_date': project.start_date,
            'end_date': project.end_date,
        }

    def generate_resource_utilization_report(self, report):
        resource = report.resource
        if not resource:
            return None

        allocations = ResourceAllocation.objects.filter(resource=resource)
        total_hours = allocations.aggregate(Sum('quantity_allocated'))['quantity_allocated__sum'] or 0
        projects_count = allocations.values('project').distinct().count()

        return {
            'resource_name': resource.name,
            'total_allocated_hours': total_hours,
            'projects_count': projects_count,
            'average_hours_per_project': round(total_hours / projects_count, 2) if projects_count > 0 else 0,
        }

    def generate_team_performance_report(self, report):
        project = report.project
        if not project:
            return None

        team_members = project.team_members.all()
        performance_data = []

        for member in team_members:
            tasks = Task.objects.filter(project=project, assigned_to=member)
            completed_tasks = tasks.filter(status='completed').count()
            total_tasks = tasks.count()
            completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

            performance_data.append({
                'member_name': member.get_full_name(),
                'completed_tasks': completed_tasks,
                'total_tasks': total_tasks,
                'completion_rate': round(completion_rate, 2),
            })

        return performance_data

    def generate_financial_summary_report(self, report):
        project = report.project
        if not project:
            return None

        total_budget = project.budget or 0
        expenses = project.expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        remaining_budget = total_budget - expenses

        return {
            'project_name': project.name,
            'total_budget': total_budget,
            'total_expenses': expenses,
            'remaining_budget': remaining_budget,
            'budget_utilization_percentage': round((expenses / total_budget) * 100, 2) if total_budget > 0 else 0,
        }

    def generate_client_overview_report(self, report):
        client = report.client
        if not client:
            return None

        projects = Project.objects.filter(client=client)
        interactions = ClientInteraction.objects.filter(client=client)

        return {
            'client_name': client.name,
            'total_projects': projects.count(),
            'active_projects': projects.filter(status='active').count(),
            'completed_projects': projects.filter(status='completed').count(),
            'total_interactions': interactions.count(),
            'last_interaction_date': interactions.order_by('-date').first().date if interactions.exists() else None,
        }

class ReportCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'reporting/report_form.html'
    success_url = reverse_lazy('reporting:report_list')
    permission_required = 'reporting.add_report'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Report created successfully.')
        return super().form_valid(form)

class ReportUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'reporting/report_form.html'
    success_url = reverse_lazy('reporting:report_list')
    permission_required = 'reporting.change_report'

    def form_valid(self, form):
        messages.success(self.request, 'Report updated successfully.')
        return super().form_valid(form)

class ReportDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Report
    template_name = 'reporting/report_confirm_delete.html'
    success_url = reverse_lazy('reporting:report_list')
    permission_required = 'reporting.delete_report'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Report deleted successfully.')
        return super().delete(request, *args, **kwargs)

class ReportScheduleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ReportSchedule
    form_class = ReportScheduleForm
    template_name = 'reporting/report_schedule_form.html'
    success_url = reverse_lazy('reporting:report_list')
    permission_required = 'reporting.add_reportschedule'

    def form_valid(self, form):
        messages.success(self.request, 'Report schedule created successfully.')
        return super().form_valid(form)

class ReportScheduleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ReportSchedule
    form_class = ReportScheduleForm
    template_name = 'reporting/report_schedule_form.html'
    success_url = reverse_lazy('reporting:report_list')
    permission_required = 'reporting.change_reportschedule'

    def form_valid(self, form):
        messages.success(self.request, 'Report schedule updated successfully.')
        return super().form_valid(form)

class ReportScheduleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ReportSchedule
    template_name = 'reporting/report_schedule_confirm_delete.html'
    success_url = reverse_lazy('reporting:report_list')
    permission_required = 'reporting.delete_reportschedule'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Report schedule deleted successfully.')
        return super().delete(request, *args, **kwargs)

def export_report_csv(request, pk):
    report = get_object_or_404(Report, pk=pk)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{report.title}.csv"'

    writer = csv.writer(response)
    report_data = report.generate_report_data()

    if report.report_type == 'project_progress':
        writer.writerow(['Project Name', 'Total Tasks', 'Completed Tasks', 'Progress Percentage', 'Start Date', 'End Date'])
        writer.writerow([
            report_data['project_name'],
            report_data['total_tasks'],
            report_data['completed_tasks'],
            f"{report_data['progress_percentage']}%",
            report_data['start_date'],
            report_data['end_date']
        ])
    elif report.report_type == 'resource_utilization':
        writer.writerow(['Resource Name', 'Total Allocated Hours', 'Projects Count', 'Average Hours per Project'])
        writer.writerow([
            report_data['resource_name'],
            report_data['total_allocated_hours'],
            report_data['projects_count'],
            report_data['average_hours_per_project']
        ])
    elif report.report_type == 'team_performance':
        writer.writerow(['Member Name', 'Completed Tasks', 'Total Tasks', 'Completion Rate'])
        for member_data in report_data:
            writer.writerow([
                member_data['member_name'],
                member_data['completed_tasks'],
                member_data['total_tasks'],
                f"{member_data['completion_rate']}%"
            ])
    elif report.report_type == 'financial_summary':
        writer.writerow(['Project Name', 'Total Budget', 'Total Expenses', 'Remaining Budget', 'Budget Utilization Percentage'])
        writer.writerow([
            report_data['project_name'],
            report_data['total_budget'],
            report_data['total_expenses'],
            report_data['remaining_budget'],
            f"{report_data['budget_utilization_percentage']}%"
        ])
    elif report.report_type == 'client_overview':
        writer.writerow(['Client Name', 'Total Projects', 'Active Projects', 'Completed Projects', 'Total Interactions', 'Last Interaction Date'])
        writer.writerow([
            report_data['client_name'],
            report_data['total_projects'],
            report_data['active_projects'],
            report_data['completed_projects'],
            report_data['total_interactions'],
            report_data['last_interaction_date']
        ])

    return response

def generate_report_chart(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report_data = report.generate_report_data()

    plt.figure(figsize=(10, 6))
    
    if report.report_type == 'project_progress':
        labels = ['Completed', 'Remaining']
        sizes = [report_data['completed_tasks'], report_data['total_tasks'] - report_data['completed_tasks']]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title(f"Project Progress: {report_data['project_name']}")
    elif report.report_type == 'resource_utilization':
        plt.bar(['Total Hours', 'Average per Project'], 
                [report_data['total_allocated_hours'], report_data['average_hours_per_project']])
        plt.title(f"Resource Utilization: {report_data['resource_name']}")
        plt.ylabel('Hours')
    elif report.report_type == 'team_performance':
        names = [data['member_name'] for data in report_data]
        completion_rates = [data['completion_rate'] for data in report_data]
        plt.bar(names, completion_rates)
        plt.title("Team Performance")
        plt.ylabel('Completion Rate (%)')
        plt.xticks(rotation=45, ha='right')
    elif report.report_type == 'financial_summary':
        labels = ['Expenses', 'Remaining']
        sizes = [report_data['total_expenses'], report_data['remaining_budget']]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title(f"Financial Summary: {report_data['project_name']}")
    elif report.report_type == 'client_overview':
        labels = ['Active', 'Completed', 'Other']
        sizes = [report_data['active_projects'], report_data['completed_projects'], 
                 report_data['total_projects'] - report_data['active_projects'] - report_data['completed_projects']]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title(f"Client Overview: {report_data['client_name']}")

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return HttpResponse(buffer.getvalue(), content_type='image/png')