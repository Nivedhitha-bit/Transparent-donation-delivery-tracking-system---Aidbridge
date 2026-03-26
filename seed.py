import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aidbridge.settings')
django.setup()

from accounts.models import User, NGOProfile, DonorProfile, VolunteerProfile
from ngo.models import DonationRequest, Donation, VolunteerAssignment, Notification

def seed():
    print("Seeding enhanced database...")

    # Clear previous mock data to prevent duplicates
    mock_usernames = ['donor1', 'donor2', 'ngo_hope', 'ngo_care', 'vol_john', 'vol_sarah']
    User.objects.filter(username__in=mock_usernames).delete()

    # 1. Create Users
    d1 = User.objects.create_user(username='donor1', password='password123', email='donor1@example.com', first_name='Alice', last_name='Donor', role='donor', city='New York', pincode='10001')
    d2 = User.objects.create_user(username='donor2', password='password123', email='donor2@example.com', first_name='Bob', last_name='Giver', role='donor', city='New York', pincode='10001')
    DonorProfile.objects.create(user=d1, total_donations=2)
    DonorProfile.objects.create(user=d2, total_donations=1)

    ngo1 = User.objects.create_user(username='ngo_hope', password='password123', email='hope@ngo.org', role='ngo', city='New York', is_verified=True, first_name='Hope', last_name='Org')
    ngo2 = User.objects.create_user(username='ngo_care', password='password123', email='care@ngo.org', role='ngo', city='Boston', is_verified=True, first_name='Care', last_name='Group')
    NGOProfile.objects.create(user=ngo1, organization_name='Hope Foundation', description='Providing food and clothes', city='New York', pincode='10001', is_approved=True)
    NGOProfile.objects.create(user=ngo2, organization_name='Care Network', description='Medical and education support', city='Boston', pincode='02115', is_approved=True)

    v1 = User.objects.create_user(username='vol_john', password='password123', email='john@vol.com', first_name='John', last_name='Doe', role='volunteer', city='New York')
    v2 = User.objects.create_user(username='vol_sarah', password='password123', email='sarah@vol.com', first_name='Sarah', last_name='Connor', role='volunteer', city='New York')
    VolunteerProfile.objects.create(user=v1, city='New York', pincode='10001', total_tasks=2, completed_tasks=1)
    VolunteerProfile.objects.create(user=v2, city='New York', pincode='10001', total_tasks=0, completed_tasks=0)

    # 2. Add Donation Requests
    req1 = DonationRequest.objects.create(ngo=ngo1, item_category='food', item_name='Rice and Groceries', quantity=100, unit='kg', city='New York', pincode='10001', location='123 Main St', quantity_received=15)
    req2 = DonationRequest.objects.create(ngo=ngo1, item_category='clothing', item_name='Winter Blankets', quantity=50, unit='pieces', city='New York', pincode='10001', location='123 Main St')
    req3 = DonationRequest.objects.create(ngo=ngo2, item_category='medical', item_name='First Aid Supplies', quantity=20, unit='packs', city='Boston', location='45 Health Ave')

    # 3. Add Donations
    don1 = Donation.objects.create(request=req1, donor=d1, item_name='Rice Sacks', quantity=10, unit='kg', status='picked_up', message='Hope this helps!')
    don2 = Donation.objects.create(request=req2, donor=d2, item_name='Warm Blankets', quantity=5, unit='pieces', status='pledged', message='Freshly washed.')
    don3 = Donation.objects.create(request=req1, donor=d1, item_name='Dal', quantity=5, unit='kg', status='delivered')

    # 4. Add Volunteer Assignments
    VolunteerAssignment.objects.create(donation=don1, volunteer=v1, ngo=ngo1, status='picked_up', pickup_location='Uptown NY', delivery_location='123 Main St')
    VolunteerAssignment.objects.create(donation=don3, volunteer=v1, ngo=ngo1, status='delivered', pickup_location='Downtown NY', delivery_location='123 Main St')

    # 5. Add Updates/Notifications for the dashboards
    # Donor notifications
    Notification.objects.create(user=d1, title='Donation Picked Up', message=f'Your donation "{don1.item_name}" has been picked up by volunteer {v1.first_name}.', link='/donor/my-donations/')
    Notification.objects.create(user=d1, title='Donation Delivered', message=f'Your donation "{don3.item_name}" was successfully delivered to {ngo1.ngo_profile.organization_name}.', link='/donor/my-donations/')
    Notification.objects.create(user=d2, title='Donation Pledged', message=f'Your pledge for "{don2.item_name}" has been registered. An NGO representative will approve it soon.', link='/donor/my-donations/')

    # NGO notifications
    Notification.objects.create(user=ngo1, title='New Pledge Received', message=f'{d2.first_name} pledged {don2.quantity} {don2.unit} of {don2.item_name}.', link='/ngo/donation-management/')
    Notification.objects.create(user=ngo1, title='Successful Delivery', message=f'Volunteer {v1.first_name} delivered {don3.item_name}.', link='/ngo/dashboard/')
    Notification.objects.create(user=ngo2, title='Profile Approved', message='Your NGO profile has been approved! You can now receive donations.', link='/ngo/dashboard/')

    # Volunteer notifications
    Notification.objects.create(user=v1, title='New Assignment', message=f'You have been assigned to pick up {don1.item_name}.', link='/volunteer/tasks/')
    Notification.objects.create(user=v1, title='Task Completed', message=f'You successfully delivered {don3.item_name}. Great job!', link='/volunteer/history/')
    Notification.objects.create(user=v2, title='Welcome Volunteer', message='Welcome to AidBridge! Browse tasks near you to get started.', link='/volunteer/browse-tasks/')

    print("Success: Enhanced mock data populated including notifications and updates.")

if __name__ == '__main__':
    seed()
