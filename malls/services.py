from django.db.models import Prefetch, QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from malls.forms import Search, FiltersForm, ImageUploadForm
from malls.models import Mall, Area


def __filter_query_set(search_request) -> QuerySet:
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


def get_search_context(request: HttpRequest) -> dict:
    search_form = Search()
    search_request = request.GET.dict()
    if search_request and search_request['search'] != '':
        malls = Mall.objects.filter(name__icontains=search_request['search'])
        if search_request['owner'] != '':
            malls = malls.filter(owner__email=search_request['owner'])
        malls = malls.prefetch_related(Prefetch('areas', queryset=__filter_query_set(search_request)))
    else:
        malls = Mall.objects.all()
    context = {'search_form': search_form, 'malls': malls}
    return context


def get_mall_detail_context(request: HttpRequest, mall_pk: int) -> dict:
    form = FiltersForm()
    search_request = request.GET.dict()
    if search_request:
        mall = get_object_or_404(Mall.objects.prefetch_related('gallery').prefetch_related(
            Prefetch('areas', queryset=__filter_query_set(search_request))), pk=mall_pk)
    else:
        mall = get_object_or_404(Mall.objects.prefetch_related('gallery', 'areas'), pk=mall_pk)
    image_form = ImageUploadForm(initial={'mall': mall_pk})
    context = {
        'mall': mall,
        'user': request.user,
        'form': form,
        'image_form': image_form
    }
    return context
