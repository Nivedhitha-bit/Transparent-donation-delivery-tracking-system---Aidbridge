from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ngo.models import VolunteerAssignment, Notification


def volunteer_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/accounts/login/')
        if request.user.role != 'volunteer':
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return wrapper


def create_notification(user, title, message, link=''):
    Notification.objects.create(user=user, title=title, message=message, link=link)


@volunteer_required
def dashboard(request):
    vol = request.user
    total = VolunteerAssignment.objects.filter(volunteer=vol).count()
    active = VolunteerAssignment.objects.filter(volunteer=vol, status__in=['assigned', 'accepted', 'picked_up']).count()
    completed = VolunteerAssignment.objects.filter(volunteer=vol, status='completed').count()
    unread = Notification.objects.filter(user=vol, is_read=False).count()
    try:
        is_available = vol.volunteer_profile.is_available
    except:
        is_available = True
    return render(request, 'volunteer/dashboard.html', {
        'total_tasks': total,
        'active_tasks': active,
        'completed_tasks': completed,
        'unread_count': unread,
        'is_available': is_available,
    })


@volunteer_required
def toggle_availability(request):
    try:
        profile = request.user.volunteer_profile
        profile.is_available = not profile.is_available
        profile.save()
    except:
        pass
    return redirect('/volunteer/dashboard/')


@volunteer_required
def my_tasks(request):
    assignments = VolunteerAssignment.objects.filter(
        volunteer=request.user
    ).select_related('donation__request__ngo__ngo_profile', 'donation__donor', 'ngo__ngo_profile')
    return render(request, 'volunteer/my_tasks.html', {'assignments': assignments})


@volunteer_required
def task_action(request, pk):
    assignment = get_object_or_404(VolunteerAssignment, pk=pk, volunteer=request.user)
    action = request.POST.get('action')

    if action == 'accept':
        assignment.status = 'accepted'
        assignment.save()
        create_notification(assignment.ngo, 'Volunteer Accepted Task',
            f'{request.user.get_full_name()} accepted the delivery task for {assignment.donation.item_name}.',
            '/ngo/delivery-tracking/')
    elif action == 'reject':
        assignment.status = 'rejected'
        assignment.save()
        create_notification(assignment.ngo, 'Volunteer Rejected Task',
            f'{request.user.get_full_name()} rejected the delivery task. Please reassign.',
            '/ngo/volunteer-assignment/')
    elif action == 'picked_up':
        assignment.status = 'picked_up'
        assignment.save()
        assignment.donation.status = 'picked_up'
        assignment.donation.save()
        create_notification(assignment.ngo, '📦 Item Picked Up',
            f'{request.user.get_full_name()} has picked up {assignment.donation.item_name}.',
            '/ngo/delivery-tracking/')
        create_notification(assignment.donation.donor, '📦 Your Donation Picked Up',
            f'A volunteer has picked up your donation of {assignment.donation.item_name}.',
            '/donor/my-donations/')
    elif action == 'delivered':
        assignment.status = 'delivered'
        assignment.save()
        assignment.donation.status = 'delivered'
        assignment.donation.save()
        if 'proof_image' in request.FILES:
            assignment.proof_image = request.FILES['proof_image']
            assignment.save()
        create_notification(assignment.ngo, '✅ Delivery Done - Confirm',
            f'{request.user.get_full_name()} has delivered {assignment.donation.item_name}. Please confirm.',
            '/ngo/delivery-confirmation/')
        create_notification(assignment.donation.donor, '🚚 Donation Delivered!',
            f'Your donation of {assignment.donation.item_name} has been delivered!',
            '/donor/my-donations/')

    messages.success(request, f'Task status updated to {assignment.status}.')
    return redirect('/volunteer/tasks/')


@volunteer_required
def task_tracking(request):
    assignments = VolunteerAssignment.objects.filter(
        volunteer=request.user
    ).select_related('donation__request__ngo__ngo_profile', 'donation__donor')
    status_steps_guide = [
        ('assigned', 'Assigned', 'NGO assigns you'),
        ('accepted', 'Accepted', 'You accept task'),
        ('picked_up', 'Picked Up', 'Item collected'),
        ('delivered', 'Delivered', 'Item dropped off'),
        ('completed', 'Completed', 'NGO confirms'),
    ]
    return render(request, 'volunteer/task_tracking.html', {
        'assignments': assignments,
        'status_steps_guide': status_steps_guide,
    })


@volunteer_required
def notifications(request):
    notifs = Notification.objects.filter(user=request.user)
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'volunteer/notifications.html', {'notifications': notifs})
