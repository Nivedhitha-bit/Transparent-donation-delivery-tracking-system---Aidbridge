from django.db import models
from accounts.models import User


CATEGORY_CHOICES = [
    ('food', 'Food Items'),
    ('clothing', 'Clothing'),
    ('hygiene', 'Hygiene & Personal Care'),
    ('medical', 'Medical Supplies'),
    ('educational', 'Educational Items'),
    ('household', 'Household Items'),
    ('electronics', 'Electronics'),
    ('miscellaneous', 'Miscellaneous'),
]

UNIT_CHOICES = [
    ('pieces', 'Pieces / Count'),
    ('kg', 'Kilograms (kg)'),
    ('g', 'Grams (g)'),
    ('litres', 'Litres'),
    ('ml', 'Millilitres (ml)'),
    ('packs', 'Packs / Boxes'),
    ('sets', 'Sets'),
]

STATUS_CHOICES = [
    ('active', 'Active'),
    ('partially_fulfilled', 'Partially Fulfilled'),
    ('fulfilled', 'Fulfilled'),
    ('closed', 'Closed'),
]


class DonationRequest(models.Model):
    ngo = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    item_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    item_name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='pieces')
    description = models.TextField(blank=True)
    location = models.CharField(max_length=300)
    city = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='active')
    quantity_received = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.item_name} - {self.ngo.ngo_profile.organization_name}"

    @property
    def quantity_remaining(self):
        return max(0, float(self.quantity) - float(self.quantity_received))

    @property
    def progress_percent(self):
        if float(self.quantity) == 0:
            return 0
        return min(100, int((float(self.quantity_received) / float(self.quantity)) * 100))


class Donation(models.Model):
    DONATION_STATUS = [
        ('pledged', 'Pledged'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('picked_up', 'Picked Up'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
    ]

    request = models.ForeignKey(DonationRequest, on_delete=models.CASCADE, related_name='donations')
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    item_name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='pieces')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=DONATION_STATUS, default='pledged')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.item_name} by {self.donor.username}"


class VolunteerAssignment(models.Model):
    ASSIGN_STATUS = [
        ('assigned', 'Assigned'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('picked_up', 'Picked Up'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
    ]

    donation = models.OneToOneField(Donation, on_delete=models.CASCADE, related_name='assignment')
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    ngo = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ngo_assignments')
    status = models.CharField(max_length=20, choices=ASSIGN_STATUS, default='assigned')
    pickup_location = models.CharField(max_length=300, blank=True)
    delivery_location = models.CharField(max_length=300, blank=True)
    proof_image = models.ImageField(upload_to='proofs/', blank=True, null=True)
    notes = models.TextField(blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Assignment: {self.donation} → {self.volunteer.username}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.title}"
