import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aidbridge.settings')
django.setup()

from accounts.models import User, NGOProfile, DonorProfile, VolunteerProfile
from ngo.models import DonationRequest, Donation, VolunteerAssignment, Notification

def seed():
    print("Seeding customized user data...")
    
    # Target Usernames
    users_to_delete = ['abc_foundations', 'nithya', 'preethi']
    User.objects.filter(username__in=users_to_delete).delete()

    # 1. Create NGO
    ngo1 = User.objects.create_user(username='abc_foundations', email='rashmim9566@gmail.com', password='Salem@123', role='ngo', is_verified=True, first_name='ABC', last_name='Foundations')
    NGOProfile.objects.create(user=ngo1, organization_name='ABC Foundations', description='Customized test NGO', city='Salem', pincode='636001', is_approved=True)

    # 2. Create Donor
    d1 = User.objects.create_user(username='nithya', email='nivedhithas994@gmail.com', password='Karur@123', role='donor', first_name='Nithya', last_name='S', city='Karur', pincode='639001')
    DonorProfile.objects.create(user=d1, total_donations=3)

    # 3. Create Volunteer
    v1 = User.objects.create_user(username='preethi', email='preethipri44@gmail.com', password='salem@123', role='volunteer', first_name='Preethi', last_name='Pri', city='Salem', pincode='636001')
    VolunteerProfile.objects.create(user=v1, city='Salem', pincode='636001', total_tasks=2, completed_tasks=1)

    # 4. Create more kinds of donation requests for abc_foundations
    req1 = DonationRequest.objects.create(ngo=ngo1, item_category='food', item_name='Wheat Flour (Atta)', quantity=50, unit='kg', city='Salem', pincode='636001', location='Salem Hub', quantity_received=5)
    req2 = DonationRequest.objects.create(ngo=ngo1, item_category='clothing', item_name='Kids Clothes', quantity=30, unit='pieces', city='Salem', pincode='636001', location='Salem Hub')
    req3 = DonationRequest.objects.create(ngo=ngo1, item_category='hygiene', item_name='Soap and Toothpaste', quantity=100, unit='packs', city='Salem', location='Salem Hub')
    req4 = DonationRequest.objects.create(ngo=ngo1, item_category='educational', item_name='Note Books', quantity=200, unit='pieces', city='Salem', location='Salem Hub')

    # 5. Create donations for nithya
    # Nithya donates Wheat Flour (picked up)
    don1 = Donation.objects.create(request=req1, donor=d1, item_name='Wheat Flour', quantity=5, unit='kg', status='picked_up', message='Here is the wheat flour!')
    # Nithya donates Kids Clothes (delivered)
    don2 = Donation.objects.create(request=req2, donor=d1, item_name='Used but clean clothes', quantity=10, unit='pieces', status='delivered', message='Hope it helps.')
    # Nithya pledges Note books (pledged)
    don3 = Donation.objects.create(request=req4, donor=d1, item_name='Note Books', quantity=50, unit='pieces', status='pledged', message='Pledging 50 notebooks')

    # Update request quantities based on Nithya's donations
    req2.quantity_received = 10
    req2.save()

    # 6. Create Volunteer Assignments for preethi
    # Preethi is assigned to pick up don1
    VolunteerAssignment.objects.create(donation=don1, volunteer=v1, ngo=ngo1, status='picked_up', pickup_location='Karur Main', delivery_location='Salem Hub', notes='Met donor at main junction.')
    # Preethi already delivered don2
    VolunteerAssignment.objects.create(donation=don2, volunteer=v1, ngo=ngo1, status='delivered', pickup_location='Karur Main', delivery_location='Salem Hub', notes='Delivered successfully.')

    # 7. Add System Notifications
    # NGO Updates
    Notification.objects.create(user=ngo1, title='New Donation Pledged', message='Donor Nithya pledged 50 Note Books.', link='/ngo/donation-management/')
    Notification.objects.create(user=ngo1, title='Items Delivered', message='Volunteer Preethi successfully delivered Kids Clothes.', link='/ngo/dashboard/')

    # Donor Updates
    Notification.objects.create(user=d1, title='Donation Picked Up', message='Your Wheat Flour donation has been collected by Volunteer Preethi.', link='/donor/my-donations/')
    Notification.objects.create(user=d1, title='Donation Reached NGO', message='Thank you! Your donation of Kids Clothes has reached ABC Foundations safely.', link='/donor/my-donations/')
    Notification.objects.create(user=d1, title='Pledge Registered', message='Your pledge for Note Books has been registered successfully.', link='/donor/my-donations/')

    # Volunteer Updates
    Notification.objects.create(user=v1, title='New Item to Pick Up', message='You are assigned to pick up Wheat Flour from Nithya.', link='/volunteer/tasks/')
    Notification.objects.create(user=v1, title='Delivery Confirmed', message='The NGO confirmed your delivery of Kids Clothes. Great work!', link='/volunteer/history/')
    
    print("Success: Customized mock data injected seamlessly.")

if __name__ == '__main__':
    seed()
