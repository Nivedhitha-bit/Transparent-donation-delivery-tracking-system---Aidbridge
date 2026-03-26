from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='donor_dashboard'),
    path('browse/', views.browse_requests, name='donor_browse'),
    path('request/<int:pk>/', views.request_detail, name='donor_request_detail'),
    path('donate/<int:pk>/', views.donate, name='donor_donate'),
    path('my-donations/', views.my_donations, name='donor_my_donations'),
    path('notifications/', views.notifications, name='donor_notifications'),
]
