from django.shortcuts import render, get_object_or_404
from django.views import View
from malls.models import Mall, Area


class DashboardView(View):
    def get(self, request):
        template = 'malls/dashboard.html'
        malls = Mall.objects.only('name')
        context = {'malls': malls}
        return render(request, template, context)


class MallDetailView(View):
    def get(self, request, pk):
        template = 'malls/mall_detail.html'
        mall = get_object_or_404(Mall.objects.prefetch_related('gallery', 'areas'), pk=pk)
        context = {'mall': mall}
        return render(request, template, context)


class AreaDetailView(View):
    def get(self, request, pk, area_pk):
        template = 'malls/area_detail.html'
        area = get_object_or_404(Area, pk=area_pk)
        context = {'area': area}
        return render(request, template, context)
