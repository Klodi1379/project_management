from django.contrib import admin
from .models import Project, Task, Comment, Notification

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'status', 'priority', 'start_date', 'end_date')
    list_filter = ('status', 'priority', 'manager')
    search_fields = ('name', 'description', 'manager__username')
    date_hierarchy = 'start_date'
    inlines = [TaskInline]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'assigned_to', 'status', 'priority', 'due_date')
    list_filter = ('status', 'priority', 'project')
    search_fields = ('name', 'description', 'assigned_to__username', 'project__name')
    date_hierarchy = 'due_date'
    inlines = [CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author', 'created_at')
    list_filter = ('author', 'created_at')
    search_fields = ('text', 'author__username', 'task__name')
    date_hierarchy = 'created_at'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'message')
    date_hierarchy = 'created_at'

# Customize admin site header and title
admin.site.site_header = "Project Management Admin"
admin.site.site_title = "Project Management Admin Portal"
admin.site.index_title = "Welcome to Project Management Portal"