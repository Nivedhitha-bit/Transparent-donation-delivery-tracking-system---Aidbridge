from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
import uuid

from .models import User, NGOProfile, DonorProfile, VolunteerProfile, PasswordResetToken


def login_view(request):
    if request.user.is_authenticated:
        return redirect_dashboard(request.user)
    
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        
        # Try email login
        user = None
        if '@' in username_or_email:
            try:
                u = User.objects.get(email=username_or_email)
                user = authenticate(request, username=u.username, password=password)
            except User.DoesNotExist:
                pass
        else:
            user = authenticate(request, username=username_or_email, password=password)
        
        if user:
            if user.role == 'ngo':
                try:
                    ngo = user.ngo_profile
                    if not ngo.is_approved:
                        messages.error(request, 'Your NGO account is pending admin approval.')
                        return render(request, 'accounts/login.html')
                except NGOProfile.DoesNotExist:
                    pass
            login(request, user)
            return redirect_dashboard(user)
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    
    return render(request, 'accounts/login.html')


def redirect_dashboard(user):
    if user.role == 'ngo':
        return redirect('/ngo/dashboard/')
    elif user.role == 'donor':
        return redirect('/donor/dashboard/')
    elif user.role == 'volunteer':
        return redirect('/volunteer/dashboard/')
    return redirect('/')


def register_view(request):
    if request.method == 'POST':
        role = request.POST.get('role', 'donor')
        full_name = request.POST.get('full_name', '')
        email = request.POST.get('email', '')
        username = request.POST.get('username', email.split('@')[0])
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        city = request.POST.get('city', '')
        pincode = request.POST.get('pincode', '')
        phone = request.POST.get('phone', '')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'accounts/register.html')

        if User.objects.filter(username=username).exists():
            username = username + str(User.objects.count())

        names = full_name.split(' ', 1)
        first_name = names[0]
        last_name = names[1] if len(names) > 1 else ''

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role,
            city=city,
            pincode=pincode,
            phone=phone,
        )

        if role == 'ngo':
            description = request.POST.get('description', '')
            NGOProfile.objects.create(
                user=user,
                organization_name=full_name,
                description=description,
                city=city,
                pincode=pincode,
            )
            # Notify admin
            try:
                send_mail(
                    'New NGO Registration - AidBridge',
                    f'NGO "{full_name}" has registered and needs approval.\nEmail: {email}\nCity: {city}',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=True,
                )
            except:
                pass
            return render(request, 'accounts/ngo_pending.html', {'org_name': full_name})

        elif role == 'donor':
            DonorProfile.objects.create(user=user)
        elif role == 'volunteer':
            VolunteerProfile.objects.create(user=user, city=city, pincode=pincode)

        messages.success(request, 'Registration successful! Please login.')
        return redirect('/accounts/login/')

    return render(request, 'accounts/register.html')


def logout_view(request):
    logout(request)
    return redirect('/')


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        try:
            user = User.objects.get(email=email)
            token = str(uuid.uuid4())
            PasswordResetToken.objects.create(user=user, token=token)
            reset_url = request.build_absolute_uri(f'/accounts/reset-password/{token}/')
            try:
                send_mail(
                    'Reset Your AidBridge Password',
                    f'''Hi {user.first_name},

Click the link below to reset your password:
{reset_url}

This link expires in 1 hour.

— AidBridge Team''',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=True,
                )
            except:
                pass
            messages.success(request, 'Password reset link sent to your email.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with that email.')
    return render(request, 'accounts/forgot_password.html')


def reset_password_view(request, token):
    reset_obj = get_object_or_404(PasswordResetToken, token=token)
    if not reset_obj.is_valid():
        messages.error(request, 'This reset link has expired.')
        return redirect('/accounts/forgot-password/')

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')
        if password != confirm:
            messages.error(request, 'Passwords do not match.')
        else:
            reset_obj.user.set_password(password)
            reset_obj.user.save()
            reset_obj.used = True
            reset_obj.save()
            messages.success(request, 'Password reset successfully. Please login.')
            return redirect('/accounts/login/')

    return render(request, 'accounts/reset_password.html', {'token': token})


@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.phone = request.POST.get('phone', user.phone)
        user.city = request.POST.get('city', user.city)
        user.pincode = request.POST.get('pincode', user.pincode)
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        new_password = request.POST.get('new_password', '')
        confirm_new = request.POST.get('confirm_new', '')
        if new_password:
            if new_password != confirm_new:
                messages.error(request, 'New passwords do not match.')
            else:
                old_password = request.POST.get('old_password', '')
                if user.check_password(old_password):
                    user.set_password(new_password)
                    messages.success(request, 'Password updated successfully.')
                else:
                    messages.error(request, 'Old password is incorrect.')
        user.save()

        if user.role == 'ngo':
            ngo = user.ngo_profile
            ngo.description = request.POST.get('description', ngo.description)
            ngo.city = request.POST.get('city', ngo.city)
            ngo.website = request.POST.get('website', ngo.website)
            ngo.save()

        messages.success(request, 'Profile updated successfully.')

    return render(request, 'accounts/profile.html', {'user': user})


def dashboard_redirect(request):
    if request.user.is_authenticated:
        return redirect_dashboard(request.user)
    return redirect('/accounts/login/')
