# AidBridge — Setup & Run Guide

## Overview
AidBridge is a full-stack Django web application connecting Donors, NGOs, and Volunteers
for transparent, trackable item-based donations.

---

## Prerequisites
- Python 3.10+
- pip
- *(No MySQL or any external database needed — uses SQLite out of the box)*

---

## Step 1 — Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

---

## Step 2 — Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs only Django and Pillow. No database drivers needed — SQLite is built into Python.

---

## Step 3 — Configure Email (Optional but Recommended)

Edit `aidbridge/settings.py` and set your Gmail SMTP credentials:

```python
EMAIL_HOST_USER = 'your_gmail@gmail.com'
EMAIL_HOST_PASSWORD = 'your_gmail_app_password'
DEFAULT_FROM_EMAIL = 'AidBridge <your_gmail@gmail.com>'
```

> **NOTE:** Use a Gmail App Password (not your regular password).
> Generate at: Google Account → Security → 2-Step Verification → App Passwords

If you skip this, the app still works — email notifications will just fail silently.
To print emails to terminal instead, add to `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

---

## Step 4 — Run Migrations

```bash
python manage.py makemigrations accounts ngo donor volunteer chatbot
python manage.py migrate
```

This creates `db.sqlite3` automatically in the project root. No manual database creation needed.

---

## Step 5 — Create Admin Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts. This account manages the admin panel at `/admin/`.

---

## Step 6 — Collect Static Files (Optional, for production)

```bash
python manage.py collectstatic
```

Not required for local development — static files are served automatically with `DEBUG = True`.

---

## Step 7 — Run the Server

```bash
python manage.py runserver
```

Open: http://127.0.0.1:8000

---

## Admin Panel
URL: http://127.0.0.1:8000/admin/
- Login with your superuser credentials
- **Approve NGOs**: Go to NGO Profiles → select NGOs → Action: "Approve selected NGOs"
- Approved NGOs receive an automatic email notification with login link

---

## Google OAuth (Optional)
1. Go to https://console.cloud.google.com/
2. Create a project → Enable Google+ API
3. Create OAuth credentials (Web Application)
4. Add http://127.0.0.1:8000 to authorized origins
5. Copy Client ID and Secret to `settings.py`:
   ```python
   GOOGLE_CLIENT_ID = 'your-client-id.apps.googleusercontent.com'
   GOOGLE_CLIENT_SECRET = 'your-secret'
   ```

---

## Project Structure

```
aidbridge/
├── aidbridge/          # Project config (settings, urls, wsgi)
├── core/               # Landing page, home, about, contact
│   ├── static/         # CSS, JS, images (bg, logo, hero photos)
│   └── templates/core/ # base.html, dashboard_base.html, home.html
├── accounts/           # Custom User model, login, register, profile
├── ngo/                # NGO dashboard, requests, donations, assignments
├── donor/              # Donor dashboard, browse, donate, tracking
├── volunteer/          # Volunteer dashboard, tasks, delivery
├── chatbot/            # Rule-based chatbot API
├── media/              # Uploaded files (proof images, profiles)
├── db.sqlite3          # Auto-created SQLite database (after migrate)
├── requirements.txt
└── manage.py
```

---

## User Roles & Workflows

### Donor
1. Register at /accounts/register/ (select Donor)
2. Login → Browse Requests → Donate Now
3. Track donations: Pledged → Approved → Picked Up → Delivered → Completed

### NGO
1. Register at /accounts/register/ (select NGO)
2. Wait for admin approval (email notification sent)
3. Login → Create Requests → Manage Donations → Assign Volunteers → Confirm Deliveries

### Volunteer
1. Register at /accounts/register/ (select Volunteer)
2. Login → Set availability ON → Accept tasks → Mark Picked Up → Mark Delivered → Upload Proof

### Admin (Superuser)
1. Login at /admin/
2. Approve NGOs (NGO Profiles → select → Approve action)
3. Monitor all users, donations, assignments

---

## Chatbot
Built-in rule-based chatbot available on ALL pages.
Click the 💬 button (bottom-right corner) to ask questions about:
- How AidBridge works
- Registration and login help
- Donation process
- NGO and volunteer guides
- Platform features

---

## Default URLs
| URL | Description |
|-----|-------------|
| / | Landing page |
| /accounts/login/ | Login |
| /accounts/register/ | Registration |
| /accounts/forgot-password/ | Password reset |
| /ngo/dashboard/ | NGO dashboard |
| /donor/dashboard/ | Donor dashboard |
| /volunteer/dashboard/ | Volunteer dashboard |
| /admin/ | Django admin panel |
| /chatbot/api/ | Chatbot API endpoint |

---

## Tech Stack
- **Backend**: Django 4.2, Python 3.10+
- **Database**: SQLite 3 (built into Python — zero configuration)
- **Frontend**: HTML5, CSS3, Vanilla JS (no framework needed)
- **Email**: Gmail SMTP
- **Auth**: Django auth + custom User model
- **Storage**: Django media files (Pillow for images)

---

## Quick Start (All Steps in One Block)

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations (creates db.sqlite3 automatically)
python manage.py makemigrations accounts ngo donor volunteer chatbot
python manage.py migrate

# 4. Create admin user
python manage.py createsuperuser

# 5. Start the server
python manage.py runserver
```

Then open http://127.0.0.1:8000

---

© 2026 AidBridge — Connecting Donors, NGOs and Volunteers
