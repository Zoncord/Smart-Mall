from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from malls.models import Mall, Area, Rent
from core.decorators import tenant_required, lessor_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from malls.forms import MallForm, AreaForm, RentForm

from malls.services import get_mall_detail_context, get_search_context


@method_decorator([login_required, lessor_required], 'get')
class DashboardView(View):
    def get(self, request):
        template = 'malls/dashboard.html'
        malls = Mall.objects.only('name').filter(owner=request.user)
        context = {
            'malls': malls,
            'user': request.user
        }
        return render(request, template, context)


class MallDetailView(View):
    def get(self, request, pk):
        template = 'malls/mall_detail.html'
        context = get_mall_detail_context(request, pk)
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


@method_decorator(lessor_required, name='get')
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
            return redirect('malls:mall_detail', pk)
        else:
            return self.get(request, pk)


@method_decorator(lessor_required, name='get')
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
            return redirect('malls:area_detail', pk, area_pk)
        else:
            return self.get(request, pk, area_pk)


@method_decorator(lessor_required, name='get')
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
            return redirect('malls:dashboard')
        else:
            return self.get(request)


@method_decorator(lessor_required, name='get')
class AreaCreateView(View):
    def get(self, request, pk):
        template = 'malls/area_create.html'
        form = AreaForm(initial={'mall': pk})
        context = {
            'form': form,
            'pk': pk
        }
        return render(request, template, context)

    def post(self, request, pk):
        form = AreaForm(request.POST, initial={'mall': pk})
        if form.is_valid():
            form.save()
            return redirect('malls:mall_detail', pk)
        else:
            return self.get(request, pk)


class MallDeleteView(View):
    def post(self, request, pk):
        mall = get_object_or_404(Mall, pk=pk)
        mall.delete()
        return redirect('malls:dashboard')


class AreaDeleteView(View):
    def post(self, request, pk, area_pk):
        area = get_object_or_404(Area, pk=area_pk)
        area.delete()
        return redirect('malls:mall_detail', pk)


class RentDetailView(View):
    def get(self, request, pk, area_pk, rent_pk):
        template = 'malls/rent_detail.html'
        rent = get_object_or_404(Rent, pk=rent_pk)
        context = {
            'rent': rent,
            'pk': pk,
            'area_pk': area_pk,
            'rent_pk': rent_pk
        }
        return render(request, template, context)


class RentEditView(View):
    def get(self, request, pk, area_pk, rent_pk):
        template = 'malls/rent_edit.html'
        rent = get_object_or_404(Rent, pk=rent_pk)
        form = RentForm(instance=rent)
        context = {
            'rent': rent,
            'pk': pk,
            'area_pk': area_pk,
            'rent_pk': rent_pk,
            'form': form
        }
        return render(request, template, context)

    def post(self, request, pk, area_pk, rent_pk):
        rent = get_object_or_404(Rent, pk=rent_pk)
        form = RentForm(request.POST, instance=rent)
        if form.is_valid():
            form.save()
            return redirect('malls:rent_detail', pk, area_pk, rent_pk)
        else:
            return self.get(request, pk, area_pk, rent_pk)


class RentCreateView(View):
    def get(self, request, pk, area_pk):
        template = 'malls/rent_create.html'
        form = RentForm(initial={'area': area_pk, 'tenant': request.user.pk})
        context = {
            'form': form,
            'pk': pk,
            'area_pk': area_pk
        }
        return render(request, template, context)

    def post(self, request, pk, area_pk):
        form = RentForm(request.POST, initial={'area': area_pk, 'tenant': request.user.pk})
        if form.is_valid():
            form.save()
            return redirect('malls:area_detail', pk, area_pk)
        else:
            return self.get(request, pk, area_pk)


class RentDeleteView(View):
    def post(self, request, pk, area_pk, rent_pk):
        rent = get_object_or_404(Rent, pk=rent_pk)
        rent.delete()
        return redirect('malls:area_detail', pk, area_pk)


class SearchView(View):
    def get(self, request):
        template = 'malls/search.html'
        context = get_search_context(request)
        return render(request, template, context)
