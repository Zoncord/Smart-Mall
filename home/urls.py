from django.urls import path
from home import views

app_name = 'home'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about')
]
