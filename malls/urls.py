from django.urls import path
from malls import views

urlpatterns = [
    path('mall/<int:pk>/area/<int:area_pk>/rent/<int:rent_pk>/edit/', views.RentEditView.as_view(), name='rent_edit'),
    path('mall/<int:pk>/area/<int:area_pk>/rent/<int:rent_pk>/delete/', views.RentDeleteView.as_view(), name='rent_delete'),
    path('mall/<int:pk>/area/<int:area_pk>/rent/<int:rent_pk>/', views.RentDetailView.as_view(), name='rent_detail'),
    path('mall/<int:pk>/area/<int:area_pk>/new/rent/', views.RentCreateView.as_view(), name='rent_create'),
    path('mall/<int:pk>/area/<int:area_pk>/edit/', views.AreaEditView.as_view(), name='area_edit'),
    path('mall/<int:pk>/area/<int:area_pk>/delete/', views.AreaDeleteView.as_view(), name='area_delete'),
    path('mall/<int:pk>/area/<int:area_pk>/', views.AreaDetailView.as_view(), name='area_detail'),
    path('mall/<int:pk>/new/area/', views.AreaCreateView.as_view(), name='area_create'),
    path('mall/<int:pk>/edit/', views.MallEditView.as_view(), name='mall_edit'),
    path('mall/<int:pk>/delete/', views.MallDeleteView.as_view(), name='mall_delete'),
    path('mall/<int:pk>/', views.MallDetailView.as_view(), name='mall_detail'),
    path('mall/new/mall/', views.MallCreateView.as_view(), name='mall_create'),
    path('', views.DashboardView.as_view(), name='home'),
    path('search/', views.SearchView.as_view(), name='search'),
]
