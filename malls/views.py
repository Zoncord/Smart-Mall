from django.shortcuts import render
from django.views import View


class DashboardView(View):
    def get(self, request):
        template = 'malls/dashboard.html'
        return render(request, template)
