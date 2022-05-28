from django.urls import include, path
from malls import views

app_name = 'malls'

rent_pk = [
    path('edit/', views.RentEditView.as_view(), name='rent_edit'),
    path('delete/', views.RentDeleteView.as_view(), name='rent_delete'),
    path('', views.RentDetailView.as_view(), name='rent_detail'),
]

area_pk = [
    path('rent/<int:rent_pk>/', include(rent_pk)),
    path('rent/new/', views.RentCreateView.as_view(), name='rent_create'),
    path('edit/', views.AreaEditView.as_view(), name='area_edit'),
    path('delete/', views.AreaDeleteView.as_view(), name='area_delete'),
    path('', views.AreaDetailView.as_view(), name='area_detail'),
]

mall_pk = [
    path('area/<int:area_pk>/', include(area_pk)),
    path('area/new/', views.AreaCreateView.as_view(), name='area_create'),
    path('edit/', views.MallEditView.as_view(), name='mall_edit'),
    path('delete/', views.MallDeleteView.as_view(), name='mall_delete'),
    path('', views.MallDetailView.as_view(), name='mall_detail'),
]

urlpatterns = [
    path('mall/<int:pk>/', include(mall_pk)),
    path('search/', views.SearchView.as_view(), name='search'),
    path('mall/new/', views.MallCreateView.as_view(), name='mall_create'),
    path('', views.DashboardView.as_view(), name='dashboard')
]