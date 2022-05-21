from urllib import response
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.views import View
from malls.models import Mall, Area, Rent
from core.decorators import tenant_required, lessor_required
from django.utils.decorators import method_decorator
from malls.forms import MallForm, AreaForm, RentForm, Search, FiltersForm
from django.db.models import Prefetch


class DashboardView(View):
    def get(self, request):
        template = 'malls/dashboard.html'
        malls = Mall.objects.only('name')
        context = {
            'malls': malls,
            'user': request.user
        }
        return render(request, template, context)

def filter_querisets(search_request):
    queryset = Area.objects.all()
    if search_request['min_square'] != '' and search_request['min_square'].isdigit():
        queryset = queryset.filter(square__gte=search_request['min_square'])
    if search_request['max_square'] != '' and search_request['max_square'].isdigit():
        queryset = queryset.filter(square__lte=search_request['max_square'])
    if search_request['min_price'] != '' and search_request['min_price'].isdigit():
        queryset = queryset.filter(price__gte=search_request['min_price'])
    if search_request['max_price'] != '' and search_request['max_price'].isdigit():
        queryset = queryset.filter(price__lte=search_request['max_price'])
    return queryset

class MallDetailView(View):
    def get(self, request, pk):
        template = 'malls/mall_detail.html'
        form = FiltersForm()
        search_request = request.GET.dict()
        if search_request:
            mall = get_object_or_404(Mall.objects.prefetch_related('gallery').prefetch_related(Prefetch('areas', queryset=filter_querisets(search_request))), pk=pk)
        else:
            mall = get_object_or_404(Mall.objects.prefetch_related('gallery', 'areas'), pk=pk)
        context = {
            'mall': mall,
            'user': request.user,
            'form': form
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
            return redirect('mall_detail', pk)
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
            return redirect('area_detail', pk, area_pk)
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
            return redirect('home')
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
            return redirect('rent_detail', pk, area_pk, rent_pk)
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
            return redirect('area_detail', pk, area_pk)
        else:
            return self.get(request, pk, area_pk)


class RentDeleteView(View):
    def post(self, request, pk, area_pk, rent_pk):
        rent = get_object_or_404(Rent, pk=rent_pk)
        rent.delete()
        return redirect('area_detail', pk, area_pk)

User = get_user_model()
    
class SearchView(View):
    def get(self, request):
        template = 'malls/search.html'
        search_form = Search()
        search_request = request.GET.dict()
        mall = None
        if search_request and search_request['search'] != '':
            mall = Mall.objects.filter(name__icontains=search_request['search'])
            if search_request['owner'] != '':
                mall = mall.filter(owner__email=search_request['owner'])
            mall = mall.prefetch_related(Prefetch('areas', queryset=filter_querisets(search_request)))
        context = {'search_form': search_form, 'malls': mall}
        return render(request, template, context)
