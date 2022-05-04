from django.urls import path
from malls import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='home')
]
