from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings


def home(request):
    return render(request, 'core/home.html')


def how_it_works(request):
    steps = [
        ('📝', 'NGO Posts a Request', 'Verified NGOs create donation requests specifying exactly what they need — items, quantity, and location.'),
        ('🔍', 'Donor Browses & Pledges', 'Donors browse active requests, filter by item type or city, and pledge donations with a single click.'),
        ('✅', 'NGO Reviews & Approves', 'The NGO reviews incoming pledges and approves or rejects based on their current requirements.'),
        ('🙋', 'Volunteer Gets Assigned', 'An NGO assigns the nearest available volunteer (matched by pincode) to pick up and deliver the donation.'),
        ('📦', 'Volunteer Picks Up', 'The volunteer accepts the task, collects the item from the donor, and marks it as picked up.'),
        ('🚚', 'Delivery & Proof Upload', 'Volunteer delivers to the NGO and uploads a photo as proof of delivery.'),
        ('🎉', 'NGO Confirms Receipt', 'The NGO verifies the delivered items and marks the donation as completed — everyone gets notified!'),
    ]
    return render(request, 'core/how_it_works.html', {'steps': steps})


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message_text = request.POST.get('message', '')
        try:
            send_mail(
                f'AidBridge Contact: {name}',
                f'From: {name} <{email}>\n\n{message_text}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],
                fail_silently=True,
            )
        except Exception:
            pass
        messages.success(request, "Your message has been sent! We'll get back to you soon.")
    return render(request, 'core/contact.html')


def dashboard_redirect(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    role = request.user.role
    if role == 'ngo':
        return redirect('/ngo/dashboard/')
    elif role == 'donor':
        return redirect('/donor/dashboard/')
    elif role == 'volunteer':
        return redirect('/volunteer/dashboard/')
    return redirect('/')
