from django.urls import path
from malls import views

urlpatterns = [
    path('mall/<int:pk>/area/<int:area_pk>/', views.AreaDetailView.as_view(), name='area_detail'),
    path('mall/<int:pk>/edit/', views.MallEditView.as_view(), name='mall_edit'),
    path('mall/<int:pk>/', views.MallDetailView.as_view(), name='mall_detail'),
    path('', views.DashboardView.as_view(), name='home')
]
