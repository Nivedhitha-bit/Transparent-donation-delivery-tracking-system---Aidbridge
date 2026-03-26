from django.contrib import admin
from .models import DonationRequest, Donation, VolunteerAssignment, Notification


@admin.register(DonationRequest)
class DonationRequestAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'ngo', 'item_category', 'quantity', 'unit', 'status', 'city', 'created_at')
    list_filter = ('status', 'item_category')
    search_fields = ('item_name', 'ngo__username', 'city')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'donor', 'request', 'quantity', 'unit', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('item_name', 'donor__username')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(VolunteerAssignment)
class VolunteerAssignmentAdmin(admin.ModelAdmin):
    list_display = ('donation', 'volunteer', 'ngo', 'status', 'assigned_at')
    list_filter = ('status',)
    search_fields = ('volunteer__username', 'ngo__username')
    readonly_fields = ('assigned_at', 'updated_at')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('user__username', 'title')
