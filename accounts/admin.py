from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import User, NGOProfile, DonorProfile, VolunteerProfile, PasswordResetToken


class NGOProfileInline(admin.StackedInline):
    model = NGOProfile
    can_delete = False
    verbose_name_plural = 'NGO Profile'
    extra = 0


class DonorProfileInline(admin.StackedInline):
    model = DonorProfile
    can_delete = False
    verbose_name_plural = 'Donor Profile'
    extra = 0


class VolunteerProfileInline(admin.StackedInline):
    model = VolunteerProfile
    can_delete = False
    verbose_name_plural = 'Volunteer Profile'
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'city', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'city')
    ordering = ('-date_joined',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('AidBridge Info', {
            'fields': ('role', 'phone', 'city', 'pincode', 'profile_picture')
        }),
    )

    def get_inlines(self, request, obj=None):
        if obj:
            if obj.role == 'ngo':
                return [NGOProfileInline]
            elif obj.role == 'donor':
                return [DonorProfileInline]
            elif obj.role == 'volunteer':
                return [VolunteerProfileInline]
        return []


@admin.register(NGOProfile)
class NGOProfileAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'user', 'city', 'is_approved', 'approved_at')
    list_filter = ('is_approved',)
    search_fields = ('organization_name', 'user__email', 'city')
    actions = ['approve_ngos', 'revoke_ngo_approval']
    readonly_fields = ('approved_at',)

    def approve_ngos(self, request, queryset):
        count = 0
        for ngo in queryset.filter(is_approved=False):
            ngo.is_approved = True
            ngo.approved_at = timezone.now()
            ngo.save()
            ngo.user.is_verified = True
            ngo.user.save()
            # Send approval email
            login_url = request.build_absolute_uri('/accounts/login/')
            try:
                send_mail(
                    '🎉 Your NGO has been Approved — AidBridge',
                    f'''Dear {ngo.organization_name},

Great news! Your NGO registration on AidBridge has been approved by our admin team.

You can now login and start posting donation requests:
{login_url}

Thank you for being part of AidBridge!

— AidBridge Admin Team''',
                    settings.DEFAULT_FROM_EMAIL,
                    [ngo.user.email],
                    fail_silently=True,
                )
            except Exception:
                pass
            count += 1
        self.message_user(request, f'{count} NGO(s) approved and notified by email.')
    approve_ngos.short_description = '✅ Approve selected NGOs'

    def revoke_ngo_approval(self, request, queryset):
        queryset.update(is_approved=False)
        for ngo in queryset:
            ngo.user.is_verified = False
            ngo.user.save()
        self.message_user(request, 'Selected NGO approvals revoked.')
    revoke_ngo_approval.short_description = '❌ Revoke NGO approval'


@admin.register(VolunteerProfile)
class VolunteerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'pincode', 'is_available', 'total_tasks', 'completed_tasks')
    list_filter = ('is_available',)
    search_fields = ('user__username', 'city', 'pincode')


@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_donations')
    search_fields = ('user__username', 'user__email')
