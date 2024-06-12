from django.views.generic import TemplateView


class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data here
        context['data'] = 'Hello, World!'
        return context
    