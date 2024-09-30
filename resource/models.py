from django.db import models
from django.conf import settings
from projects.models import Project

class ResourceCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Resource(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ResourceCategory, on_delete=models.SET_NULL, null=True, related_name='resources')
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=1)
    acquisition_date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status_choices = [
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='available')
    last_maintenance = models.DateField(null=True, blank=True)
    next_maintenance = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class ResourceAllocation(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='allocations')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='resource_allocations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='resource_allocations')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    quantity_allocated = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.resource.name} allocated to {self.project.name}"

class MaintenanceLog(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='maintenance_logs')
    maintenance_date = models.DateField()
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Maintenance for {self.resource.name} on {self.maintenance_date}"