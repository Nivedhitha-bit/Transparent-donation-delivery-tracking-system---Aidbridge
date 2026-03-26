import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aidbridge.settings')
django.setup()

from accounts.models import User
from ngo.models import DonationRequest, Donation, VolunteerAssignment, Notification

def run_workflow():
    print("Executing the workflow automatically...")

    ngo1 = User.objects.get(username='abc_foundations')
    donor1 = User.objects.get(username='nithya')
    vol1 = User.objects.get(username='preethi')

    # 1. NGO creates a new request
    print("NGO creating request...")
    new_req = DonationRequest.objects.create(
        ngo=ngo1, item_category='medical', item_name='Emergency First Aid Kits',
        quantity=50, unit='packs', city='Salem', pincode='636001', location='Main Hospital Road'
    )
    
    # 2. Donor makes a donation
    print("Donor making donation...")
    new_donation = Donation.objects.create(
        request=new_req, donor=donor1, item_name='First Aid Kits',
        quantity=10, unit='packs', status='pledged', message='Happy to supply these kits!'
    )
    # Update Donor profile counts
    donor1.donor_profile.total_donations += 1
    donor1.donor_profile.save()
    
    # Notify NGO about pledge
    Notification.objects.create(user=ngo1, title='New Pledge Received', message=f'{donor1.first_name} pledged 10 packs of First Aid Kits.', link='/ngo/donation-management/')

    # 3. Volunteer accepts the task and sets to Picked Up
    print("Volunteer accepting and updating task...")
    # Change donation status
    new_donation.status = 'picked_up'
    new_donation.save()
    
    assignment = VolunteerAssignment.objects.create(
        donation=new_donation, volunteer=vol1, ngo=ngo1, status='picked_up',
        pickup_location='Karur Main', delivery_location='Main Hospital Road', notes='Task accepted and picked up.'
    )
    # Update Volunteer counts
    vol1.volunteer_profile.total_tasks += 1
    vol1.volunteer_profile.save()

    # Notify Donor
    Notification.objects.create(user=donor1, title='Donation Picked Up', message='Your First Aid Kits have been picked up!', link='/donor/my-donations/')

    # 4. Volunteer delivers the task
    print("Volunteer marking as delivered...")
    new_donation.status = 'delivered'
    new_donation.save()
    
    assignment.status = 'delivered'
    assignment.notes = 'Delivered safely to NGO.'
    assignment.save()
    
    # Update Volunteer completion
    vol1.volunteer_profile.completed_tasks += 1
    vol1.volunteer_profile.save()

    # Update Request received counts
    new_req.quantity_received += 10
    new_req.save()

    # Notify NGO
    Notification.objects.create(user=ngo1, title='Items Delivered', message='Volunteer Preethi successfully delivered First Aid Kits.', link='/ngo/dashboard/')

    print("Workflow complete! Dashboards are fully updated.")

if __name__ == '__main__':
    run_workflow()
