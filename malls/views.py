from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from malls.models import Mall, Area
from malls.forms import MallForm


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
        context = {
            'mall': mall,
            'user': request.user
        }
        return render(request, template, context)


class AreaDetailView(View):
    def get(self, request, pk, area_pk):
        template = 'malls/area_detail.html'
        area = get_object_or_404(Area, pk=area_pk)
        context = {'area': area}
        return render(request, template, context)


class MallEditView(View):
    def get(self, request, pk):
        template = 'malls/mall_edit.html'
        mall = get_object_or_404(Mall, pk=pk)
        form = MallForm(instance=mall)
        context = {
            'mall': mall,
            'form': form
        }
        return render(request, template, context)

    def post(self, request, pk):
        mall = get_object_or_404(Mall, pk=pk)
        form = MallForm(request.POST, instance=mall)
        if form.is_valid():
            form.save()
            return redirect('mall_detail', pk)
        else:
            return self.get(request, pk)
