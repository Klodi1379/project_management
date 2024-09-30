from django.db import models
from django.conf import settings
from projects.models import Project
from resource.models import Resource
from crm.models import Client

class Report(models.Model):
    REPORT_TYPES = [
        ('project_progress', 'Project Progress'),
        ('resource_utilization', 'Resource Utilization'),
        ('team_performance', 'Team Performance'),
        ('financial_summary', 'Financial Summary'),
        ('client_overview', 'Client Overview'),
    ]

    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_generated = models.DateTimeField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    resource = models.ForeignKey(Resource, on_delete=models.SET_NULL, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    date_range_start = models.DateField(null=True, blank=True)
    date_range_end = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.title

class ReportSchedule(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='schedules')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    recipients = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='report_subscriptions')
    is_active = models.BooleanField(default=True)
    last_sent = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.report.title} - {self.get_frequency_display()} Schedule"