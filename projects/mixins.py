from django.contrib.auth.mixins import LoginRequiredMixin

class NotificationContextMixin(LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['unread_notifications_count'] = self.request.user.project_notifications.filter(is_read=False).count()
        return context