from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from malls.models import Mall, Area
from malls.forms import MallForm, AreaForm


class DashboardView(View):
    def get(self, request):
        template = 'malls/dashboard.html'
        malls = Mall.objects.only('name')
        context = {
            'malls': malls,
            'user': request.user
        }
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
        context = {
            'area': area,
            'pk': pk
        }
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


class AreaEditView(View):
    def get(self, request, pk, area_pk):
        template = 'malls/area_edit.html'
        area = get_object_or_404(Area, pk=area_pk)
        form = AreaForm(instance=area)
        context = {
            'area': area,
            'pk': pk,
            'form': form
        }
        return render(request, template, context)

    def post(self, request, pk, area_pk):
        area = get_object_or_404(Area, pk=area_pk)
        form = AreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            return redirect('area_detail', pk, area_pk)
        else:
            return self.get(request, pk, area_pk)


class MallCreateView(View):
    def get(self, request):
        template = 'malls/mall_create.html'
        form = MallForm(initial={'owner': request.user.pk})
        context = {'form': form}
        return render(request, template, context)

    def post(self, request):
        form = MallForm(request.POST, initial={'owner': request.user.pk})
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return self.get(request)


class AreaCreateView(View):
    def get(self, request, pk):
        template = 'malls/area_create.html'
        mall = get_object_or_404(Mall, pk=pk)
        form = AreaForm(initial={'mall': mall.pk})
        context = {
            'form': form,
            'pk': pk
        }
        return render(request, template, context)

    def post(self, request, pk):
        mall = get_object_or_404(Mall, pk=pk)
        form = AreaForm(request.POST, initial={'mall': mall.pk})
        if form.is_valid():
            form.save()
            return redirect('mall_detail', pk)
        else:
            return self.get(request, pk)


class MallDeleteView(View):
    def post(self, request, pk):
        mall = get_object_or_404(Mall, pk=pk)
        mall.delete()
        return redirect('home')


class AreaDeleteView(View):
    def post(self, request, pk, area_pk):
        area = get_object_or_404(Area, pk=area_pk)
        area.delete()
        return redirect('mall_detail', pk)
