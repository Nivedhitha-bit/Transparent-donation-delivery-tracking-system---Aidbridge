from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re

RULES = [
    # Greetings
    (r'\b(hi|hello|hey|howdy)\b', "👋 Hello! Welcome to AidBridge! I'm here to help you understand how our donation platform works. Ask me anything about donating, NGOs, volunteering, or how the platform works!"),
    (r'\bthank(s| you)\b', "You're welcome! 😊 Is there anything else I can help you with?"),
    (r'\bbye|goodbye|exit\b', "Goodbye! Thank you for being part of AidBridge — together we're making a difference! 💙"),

    # What is AidBridge
    (r'what is aidbridge|about aidbridge|tell me about', "🌟 **AidBridge** is a transparent donation and delivery tracking platform that connects **Donors**, **NGOs**, and **Volunteers**.\n\n- 👤 **Donors** donate items they no longer need\n- 🏢 **NGOs** post requirements and receive donations\n- 🙋 **Volunteers** pick up and deliver donations\n\nAll activity is tracked transparently from pledge to delivery!"),
    (r'how does.*work|how it works', "Here's how AidBridge works:\n\n1️⃣ **NGO** posts a donation request (e.g., 100 notebooks)\n2️⃣ **Donor** browses requests and pledges a donation\n3️⃣ **NGO** approves the donation\n4️⃣ **NGO** assigns a nearby **Volunteer**\n5️⃣ **Volunteer** picks up and delivers the item\n6️⃣ **NGO** confirms receipt — donation marked complete!\n\nEvery step is tracked and both donor & volunteer get notified! 🎉"),

    # Registration / Login
    (r'register|sign.?up|create account', "To register on AidBridge:\n\n1. Click **Register** on the top navigation\n2. Choose your role: **Donor**, **NGO**, or **Volunteer**\n3. Fill in your details\n4. Click **Sign Up**\n\n⚠️ **NGOs** need admin approval before they can log in. You'll receive an email once approved!"),
    (r'login|sign.?in|log in', "To login:\n1. Click **Login** on the navbar\n2. Select your role\n3. Enter your email/username and password\n4. Click **Login**\n\nForgot your password? Use the **Forgot Password** link on the login page!"),
    (r'forgot.?password|reset.?password', "To reset your password:\n1. Click **Forgot Password** on the login page\n2. Enter your registered email\n3. Check your inbox for a reset link\n4. Click the link and set a new password\n\nThe link expires in **1 hour** for security."),
    (r'google.*login|login.*google|sign in.*google', "You can sign in with Google!\n1. Click **Sign in with Google** on the login page\n2. Select your Google account\n3. If new, choose your role during first login\n\nNo password needed — Google handles authentication securely! 🔐"),

    # Donor
    (r'how.*donate|donate.*how|i want to donate|start donating', "To make a donation:\n\n1. **Login** as a Donor\n2. Go to **Browse Requests** in your dashboard\n3. Filter by item type or location\n4. Click **View Details** on a request\n5. Click **Donate Now** and fill the form\n6. Your donation is now **Pledged** ✅\n\nStatus flow: Pledged → Approved → Picked Up → Delivered → Completed"),
    (r'donor.*dashboard|my donations|donation status', "Your **Donor Dashboard** has:\n\n📊 **Overview** – Total, active, completed donations\n🔍 **Browse Requests** – Find NGO needs near you\n💝 **My Donations** – Track all your donations with status\n🔔 **Notifications** – Real-time updates\n👤 **Profile** – Edit your info"),
    (r'donation.*status|status.*donation|track.*donation', "Donation status flow:\n\n🟡 **Pledged** – You've committed to donate\n✅ **Approved** – NGO accepted your donation\n📦 **Picked Up** – Volunteer collected it\n🚚 **Delivered** – Delivered to NGO\n🎉 **Completed** – NGO confirmed receipt\n\nYou get notified at each step!"),

    # NGO
    (r'ngo.*register|register.*ngo|how.*ngo.*join', "To register as an NGO:\n\n1. Go to **Register** → Select **NGO**\n2. Enter organization name, email, description, city, pincode\n3. Submit registration\n4. **Wait for admin approval** (you'll get a confirmation email)\n5. Once approved, click the login link in the email!\n\nAdmin verifies NGO authenticity before granting access."),
    (r'ngo.*dashboard|ngo.*features', "The **NGO Dashboard** includes:\n\n📋 **Overview** – Stats at a glance\n➕ **Create Request** – Post what you need\n📦 **Donation Management** – Accept/reject donations\n🙋 **Volunteer Assignment** – Assign nearby volunteers\n🚚 **Delivery Tracking** – Live status updates\n✅ **Delivery Confirmation** – Confirm & complete\n🔔 **Notifications** – All updates"),
    (r'create.*request|post.*request|ngo.*need', "To create a donation request as an NGO:\n\n1. Go to **Create Request** in your dashboard\n2. Select **Item Category** (food, clothing, medical, etc.)\n3. Enter **Item Name**, **Quantity**, and **Unit**\n4. Add **Location** and optional description\n5. Submit — donors will see it immediately!"),
    (r'approve.*ngo|ngo.*approval|admin.*approve', "NGO approval process:\n\n1. NGO submits registration\n2. Admin reviews the application in the **Admin Panel**\n3. Admin marks it as **Approved**\n4. NGO receives an **email notification** with a login link\n\nThis ensures only genuine NGOs operate on AidBridge!"),

    # Volunteer
    (r'volunteer.*dashboard|volunteer.*features', "The **Volunteer Dashboard** includes:\n\n📊 **Overview** – Tasks assigned, active, completed\n✅ **Availability Toggle** – Set yourself available/unavailable\n📋 **My Tasks** – Accept/reject & update task status\n🔄 **Task Tracking** – Full status history\n🔔 **Notifications** – Updates from NGOs"),
    (r'how.*volunteer|become.*volunteer|volunteer.*work', "As a Volunteer:\n\n1. **Register** as Volunteer with your city & pincode\n2. NGOs can see you and assign delivery tasks\n3. You get **notified** when assigned a task\n4. **Accept** or reject the task\n5. If accepted: **Mark Picked Up** → **Mark Delivered** → **Upload Proof photo**\n6. NGO confirms → Task complete!\n\nTask flow: Assigned → Accepted → Picked Up → Delivered → Completed"),
    (r'volunteer.*assign|assign.*volunteer|nearby.*volunteer', "NGOs assign volunteers based on **location matching** (city/pincode). The NGO sees available volunteers and picks the nearest one. Volunteers are notified instantly when assigned!"),
    (r'upload.*proof|delivery.*proof|proof.*photo', "After delivering items, volunteers should:\n1. Click **Mark as Delivered** on the task\n2. **Upload a photo** as proof of delivery\n3. The NGO reviews the photo and confirms\n\nThis ensures transparency and trust! 📸"),

    # Admin
    (r'admin|super.?user|admin.*panel', "The **Admin** (superuser) manages:\n\n✅ **Approve NGOs** – Verify and grant access\n👥 **Monitor Users** – Donors, volunteers, NGOs\n📊 **View Donations** – All activity\n🚚 **Volunteer Tasks** – Monitor deliveries\n🛠️ **Handle Issues** – Resolve disputes\n\nAdmin uses Django's built-in Admin Panel at `/admin/`"),

    # Items / Categories
    (r'what.*item|item.*categ|what.*donate|categories', "AidBridge accepts these item categories:\n\n🍚 Food Items\n👕 Clothing\n🧴 Hygiene & Personal Care\n💊 Medical Supplies\n📚 Educational Items\n🏠 Household Items\n📱 Electronics\n📦 Miscellaneous\n\nEach NGO posts specific items they need!"),
    (r'quantity.*unit|units.*used|how.*measure', "AidBridge uses smart quantity units:\n\n🔢 **Pieces/Count** – clothes, books, blankets\n⚖️ **Kg / Grams** – rice, vegetables, fruits\n🥛 **Litres / ml** – milk, oil, sanitizer\n📦 **Packs / Boxes** – medicines, biscuits\n🧩 **Sets** – utensil sets, etc."),

    # Notifications
    (r'notification|alert|update', "AidBridge sends notifications for:\n\n🔔 New donation received (NGO)\n✅ Donation approved/rejected (Donor)\n🙋 Volunteer assigned (Volunteer)\n📦 Item picked up (NGO & Donor)\n🚚 Delivered (NGO & Donor)\n🎉 Task completed (Volunteer)"),

    # Transparency / Trust
    (r'transparent|trust|safe|secure|verified', "AidBridge ensures transparency through:\n\n🔒 **Verified NGOs** – Admin-approved only\n📍 **Location-based matching** – Right volunteer, right place\n📸 **Proof of delivery** – Photo evidence\n📊 **Real-time tracking** – Every step visible\n✉️ **Email notifications** – All parties informed"),

    # Contact / Help
    (r'contact|help|support|issue|problem', "Need help? Here are your options:\n\n📧 Email us at **support@aidbridge.org**\n📞 Or use the **Contact** page in the main navigation\n\nFor admin-level issues, please contact your AidBridge administrator."),

    # Fallback
]

DEFAULT_RESPONSE = "🤔 I didn't quite understand that. Here are some things I can help with:\n\n• How AidBridge works\n• How to register (Donor / NGO / Volunteer)\n• How to donate or track donations\n• NGO dashboard features\n• Volunteer tasks & delivery\n• Admin panel info\n\nTry asking something like: *'How do I donate?'* or *'How does AidBridge work?'*"


def get_bot_response(message):
    message_lower = message.lower().strip()
    for pattern, response in RULES:
        if re.search(pattern, message_lower):
            return response
    return DEFAULT_RESPONSE


@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            if not user_message:
                return JsonResponse({'response': 'Please type a message!'})
            response = get_bot_response(user_message)
            return JsonResponse({'response': response})
        except Exception as e:
            return JsonResponse({'response': 'Sorry, something went wrong. Please try again.'})
    return JsonResponse({'error': 'POST required'}, status=405)
