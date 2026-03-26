from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('donor', 'Donor'),
        ('ngo', 'NGO'),
        ('volunteer', 'Volunteer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='donor')
    phone = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    is_verified = models.BooleanField(default=False)  # for NGOs
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def display_name(self):
        return self.get_full_name() or self.username


class NGOProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ngo_profile')
    organization_name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    website = models.URLField(blank=True)
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    approval_email_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.organization_name


class DonorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='donor_profile')
    total_donations = models.IntegerField(default=0)

    def __str__(self):
        return f"Donor: {self.user.username}"


class VolunteerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='volunteer_profile')
    is_available = models.BooleanField(default=True)
    city = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    total_tasks = models.IntegerField(default=0)
    completed_tasks = models.IntegerField(default=0)

    def __str__(self):
        return f"Volunteer: {self.user.username}"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def is_valid(self):
        from django.utils import timezone
        from datetime import timedelta
        return not self.used and (timezone.now() - self.created_at) < timedelta(hours=1)
