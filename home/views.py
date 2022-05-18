from django.shortcuts import render
from django.views import View


class HomePageView(View):
    def get(self, request):
        template = 'home/homepage.html'
        context = {}
        return render(request, template, context)


class AboutView(View):
    def get(self, request):
        template = 'home/about.html'
        context = {}
        return render(request, template, context)
