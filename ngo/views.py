from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

from accounts.models import User, VolunteerProfile
from .models import DonationRequest, Donation, VolunteerAssignment, Notification


def ngo_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/accounts/login/')
        if request.user.role != 'ngo':
            return redirect('/')
        try:
            if not request.user.ngo_profile.is_approved:
                return render(request, 'accounts/ngo_pending.html')
        except:
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return wrapper


def create_notification(user, title, message, link=''):
    Notification.objects.create(user=user, title=title, message=message, link=link)


@ngo_required
def dashboard(request):
    ngo = request.user
    total_requests = DonationRequest.objects.filter(ngo=ngo).count()
    active_requests = DonationRequest.objects.filter(ngo=ngo, status='active').count()
    total_donations = Donation.objects.filter(request__ngo=ngo).count()
    completed = Donation.objects.filter(request__ngo=ngo, status='completed').count()
    recent_donations = Donation.objects.filter(request__ngo=ngo).select_related('donor', 'request')[:10]
    unread_notifications = Notification.objects.filter(user=ngo, is_read=False).count()
    
    return render(request, 'ngo/dashboard.html', {
        'total_requests': total_requests,
        'active_requests': active_requests,
        'total_donations': total_donations,
        'completed_deliveries': completed,
        'recent_donations': recent_donations,
        'unread_count': unread_notifications,
    })


@ngo_required
def create_request(request):
    from .models import CATEGORY_CHOICES, UNIT_CHOICES
    if request.method == 'POST':
        req = DonationRequest.objects.create(
            ngo=request.user,
            item_category=request.POST.get('item_category'),
            item_name=request.POST.get('item_name'),
            quantity=request.POST.get('quantity'),
            unit=request.POST.get('unit'),
            description=request.POST.get('description', ''),
            location=request.POST.get('location'),
            city=request.POST.get('city', ''),
            pincode=request.POST.get('pincode', ''),
        )
        messages.success(request, f'Request for "{req.item_name}" created successfully!')
        return redirect('/ngo/manage-requests/')
    
    return render(request, 'ngo/create_request.html', {
        'categories': CATEGORY_CHOICES,
        'units': UNIT_CHOICES,
    })


@ngo_required
def manage_requests(request):
    from .models import CATEGORY_CHOICES
    requests_qs = DonationRequest.objects.filter(ngo=request.user)
    return render(request, 'ngo/manage_requests.html', {
        'requests': requests_qs,
        'categories': CATEGORY_CHOICES,
    })


@ngo_required
def edit_request(request, pk):
    from .models import CATEGORY_CHOICES, UNIT_CHOICES
    req = get_object_or_404(DonationRequest, pk=pk, ngo=request.user)
    if request.method == 'POST':
        req.item_category = request.POST.get('item_category', req.item_category)
        req.item_name = request.POST.get('item_name', req.item_name)
        req.quantity = request.POST.get('quantity', req.quantity)
        req.unit = request.POST.get('unit', req.unit)
        req.description = request.POST.get('description', req.description)
        req.location = request.POST.get('location', req.location)
        req.city = request.POST.get('city', req.city)
        req.pincode = request.POST.get('pincode', req.pincode)
        req.status = request.POST.get('status', req.status)
        req.save()
        messages.success(request, 'Request updated successfully.')
        return redirect('/ngo/manage-requests/')
    return render(request, 'ngo/edit_request.html', {
        'req': req, 'categories': CATEGORY_CHOICES, 'units': UNIT_CHOICES
    })


@ngo_required
def delete_request(request, pk):
    req = get_object_or_404(DonationRequest, pk=pk, ngo=request.user)
    if request.method == 'POST':
        req.delete()
        messages.success(request, 'Request deleted.')
    return redirect('/ngo/manage-requests/')


@ngo_required
def donation_management(request):
    donations = Donation.objects.filter(request__ngo=request.user).select_related('donor', 'request')
    return render(request, 'ngo/donation_management.html', {'donations': donations})


@ngo_required
def donation_action(request, pk):
    donation = get_object_or_404(Donation, pk=pk, request__ngo=request.user)
    action = request.POST.get('action')
    
    if action == 'approve':
        donation.status = 'approved'
        donation.save()
        create_notification(donation.donor, 'Donation Approved!',
            f'Your donation of {donation.quantity} {donation.unit} of {donation.item_name} has been approved by {request.user.ngo_profile.organization_name}.',
            '/donor/my-donations/')
        messages.success(request, 'Donation approved.')
    elif action == 'reject':
        donation.status = 'rejected'
        donation.save()
        create_notification(donation.donor, 'Donation Update',
            f'Your donation of {donation.item_name} was not accepted at this time.',
            '/donor/my-donations/')
        messages.info(request, 'Donation rejected.')
    
    return redirect('/ngo/donation-management/')


@ngo_required
def volunteer_assignment(request):
    # Get approved donations without assignment
    approved_donations = Donation.objects.filter(
        request__ngo=request.user, status='approved'
    ).exclude(assignment__isnull=False).select_related('donor', 'request')
    
    # Get volunteers by city/pincode match
    ngo_pincode = request.user.pincode or request.user.city
    volunteers = User.objects.filter(role='volunteer').select_related('volunteer_profile')
    
    assignments = VolunteerAssignment.objects.filter(ngo=request.user).select_related(
        'volunteer', 'donation__request', 'donation__donor'
    )
    
    return render(request, 'ngo/volunteer_assignment.html', {
        'approved_donations': approved_donations,
        'volunteers': volunteers,
        'assignments': assignments,
    })


@ngo_required
def assign_volunteer(request):
    if request.method == 'POST':
        donation_id = request.POST.get('donation_id')
        volunteer_id = request.POST.get('volunteer_id')
        donation = get_object_or_404(Donation, pk=donation_id, request__ngo=request.user)
        volunteer = get_object_or_404(User, pk=volunteer_id, role='volunteer')
        
        VolunteerAssignment.objects.update_or_create(
            donation=donation,
            defaults={
                'volunteer': volunteer,
                'ngo': request.user,
                'pickup_location': donation.donor.city or '',
                'delivery_location': request.user.ngo_profile.city,
                'status': 'assigned',
            }
        )
        donation.status = 'approved'
        donation.save()
        
        create_notification(volunteer, 'New Delivery Task!',
            f'You have been assigned to deliver {donation.item_name} for {request.user.ngo_profile.organization_name}.',
            '/volunteer/tasks/')
        messages.success(request, f'Volunteer {volunteer.get_full_name()} assigned successfully.')
    
    return redirect('/ngo/volunteer-assignment/')


@ngo_required
def delivery_tracking(request):
    assignments = VolunteerAssignment.objects.filter(ngo=request.user).select_related(
        'volunteer', 'donation__request', 'donation__donor'
    )
    return render(request, 'ngo/delivery_tracking.html', {'assignments': assignments})


@ngo_required
def delivery_confirmation(request):
    assignments = VolunteerAssignment.objects.filter(
        ngo=request.user, status='delivered'
    ).select_related('volunteer', 'donation__request', 'donation__donor')
    return render(request, 'ngo/delivery_confirmation.html', {'assignments': assignments})


@ngo_required
def confirm_delivery(request, pk):
    assignment = get_object_or_404(VolunteerAssignment, pk=pk, ngo=request.user)
    if request.method == 'POST':
        assignment.status = 'completed'
        assignment.save()
        assignment.donation.status = 'completed'
        assignment.donation.save()
        
        req = assignment.donation.request
        req.quantity_received = float(req.quantity_received) + float(assignment.donation.quantity)
        req.save()
        
        # Notify donor
        create_notification(assignment.donation.donor, '🎉 Donation Completed!',
            f'Your donation of {assignment.donation.item_name} has been successfully delivered and confirmed!',
            '/donor/my-donations/')
        # Notify volunteer
        create_notification(assignment.volunteer, 'Task Completed!',
            f'Your delivery task for {assignment.donation.item_name} has been confirmed. Thank you!',
            '/volunteer/tasks/')
        
        messages.success(request, 'Delivery confirmed!')
    return redirect('/ngo/delivery-confirmation/')


@ngo_required
def notifications(request):
    notifs = Notification.objects.filter(user=request.user)
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'ngo/notifications.html', {'notifications': notifs})
