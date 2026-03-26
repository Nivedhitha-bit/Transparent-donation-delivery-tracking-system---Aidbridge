from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='volunteer_dashboard'),
    path('toggle-availability/', views.toggle_availability, name='volunteer_toggle'),
    path('tasks/', views.my_tasks, name='volunteer_tasks'),
    path('task-action/<int:pk>/', views.task_action, name='volunteer_task_action'),
    path('task-tracking/', views.task_tracking, name='volunteer_tracking'),
    path('notifications/', views.notifications, name='volunteer_notifications'),
]
