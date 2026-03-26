from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ngo.models import DonationRequest, Donation, Notification


def donor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/accounts/login/')
        if request.user.role != 'donor':
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return wrapper


def create_notification(user, title, message, link=''):
    Notification.objects.create(user=user, title=title, message=message, link=link)


@donor_required
def dashboard(request):
    donor = request.user
    total = Donation.objects.filter(donor=donor).count()
    active = Donation.objects.filter(donor=donor, status__in=['pledged', 'approved', 'picked_up', 'delivered']).count()
    completed = Donation.objects.filter(donor=donor, status='completed').count()
    recent = Donation.objects.filter(donor=donor).select_related('request__ngo')[:5]
    unread = Notification.objects.filter(user=donor, is_read=False).count()
    return render(request, 'donor/dashboard.html', {
        'total_donations': total,
        'active_donations': active,
        'completed_donations': completed,
        'recent_donations': recent,
        'unread_count': unread,
    })


@donor_required
def browse_requests(request):
    requests_qs = DonationRequest.objects.filter(status='active').select_related('ngo__ngo_profile')
    item_type = request.GET.get('item_type', '')
    location = request.GET.get('location', '')
    if item_type:
        requests_qs = requests_qs.filter(item_category=item_type)
    if location:
        requests_qs = requests_qs.filter(city__icontains=location)
    from ngo.models import CATEGORY_CHOICES
    return render(request, 'donor/browse_requests.html', {
        'requests': requests_qs,
        'categories': CATEGORY_CHOICES,
        'filter_type': item_type,
        'filter_location': location,
    })


@donor_required
def request_detail(request, pk):
    req = get_object_or_404(DonationRequest, pk=pk, status='active')
    return render(request, 'donor/request_detail.html', {'req': req})


@donor_required
def donate(request, pk):
    req = get_object_or_404(DonationRequest, pk=pk, status='active')
    from ngo.models import UNIT_CHOICES
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        unit = request.POST.get('unit', req.unit)
        message = request.POST.get('message', '')
        donation = Donation.objects.create(
            request=req,
            donor=request.user,
            item_name=req.item_name,
            quantity=quantity,
            unit=unit,
            message=message,
            status='pledged',
        )
        # Notify NGO
        create_notification(req.ngo, 'New Donation Received!',
            f'{request.user.get_full_name() or request.user.username} pledged {quantity} {unit} of {req.item_name}.',
            '/ngo/donation-management/')
        messages.success(request, 'Thank you! Your donation has been pledged.')
        return redirect('/donor/my-donations/')
    return render(request, 'donor/donate.html', {'req': req, 'units': UNIT_CHOICES})


@donor_required
def my_donations(request):
    donations = Donation.objects.filter(donor=request.user).select_related('request__ngo__ngo_profile')
    return render(request, 'donor/my_donations.html', {'donations': donations})


@donor_required
def notifications(request):
    notifs = Notification.objects.filter(user=request.user)
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'donor/notifications.html', {'notifications': notifs})
