from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
]
