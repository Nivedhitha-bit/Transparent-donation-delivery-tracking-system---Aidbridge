from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='ngo_dashboard'),
    path('create-request/', views.create_request, name='ngo_create_request'),
    path('manage-requests/', views.manage_requests, name='ngo_manage_requests'),
    path('edit-request/<int:pk>/', views.edit_request, name='ngo_edit_request'),
    path('delete-request/<int:pk>/', views.delete_request, name='ngo_delete_request'),
    path('donation-management/', views.donation_management, name='ngo_donation_management'),
    path('donation-action/<int:pk>/', views.donation_action, name='ngo_donation_action'),
    path('volunteer-assignment/', views.volunteer_assignment, name='ngo_volunteer_assignment'),
    path('assign-volunteer/', views.assign_volunteer, name='ngo_assign_volunteer'),
    path('delivery-tracking/', views.delivery_tracking, name='ngo_delivery_tracking'),
    path('delivery-confirmation/', views.delivery_confirmation, name='ngo_delivery_confirmation'),
    path('confirm-delivery/<int:pk>/', views.confirm_delivery, name='ngo_confirm_delivery'),
    path('notifications/', views.notifications, name='ngo_notifications'),
]
