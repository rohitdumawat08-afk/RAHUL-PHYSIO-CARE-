# Rahul Physio – Home Visit Physiotherapy Website

A modern, responsive healthcare website and dynamic therapy/service management system for **Rahul Physio – Home Visit Physiotherapy** in Jaipur, India.

---

## Key Features

1. **Public Website**:
   - **Hero Section**: Headline, subheading, trust badges, operating hours, direct call & WhatsApp links.
   - **About Section**: Clear, ethical overview of home-based rehabilitation and 4-step treatment journey.
   - **Conditions / Specializations**: 6 interactive clinical category cards.
   - **Searchable & Filterable Therapy Catalogue**: Real-time category pills and search filter with 58 pre-seeded clinical therapies.
   - **Therapy Detail Modal**: Complete clinical description, indications, duration, and direct appointment booking.
   - **Clinical Experience**: Transparent clinical exposure timeline (Ram Sihag Neuro Physio Hospital, Chiranjivi Clinic, Welton Orthopaedic Hospital, City Rehab Sports Clinic).
   - **Jaipur Service Areas**: Interactive locality availability checker covering Sitapura, Pratap Nagar, Sanganer, Durgapura, Gopalpura, Vaishali Nagar, and more.
   - **Appointment Booking System**: Multi-step booking form with direct WhatsApp pre-filled confirmation link.
   - **Contact & Operating Hours**: Morning (6:00 AM – 2:00 PM) and Night (9:00 PM – 12:00 AM) slots, direct call, and contact form.
   - **Floating Action Widgets**: Instant call and WhatsApp buttons for mobile users.

2. **Admin Management System**:
   - Secure login portal (`/admin/login`).
   - Dashboard with stats (Total Therapies, Active, Inactive, Total Bookings, Pending Bookings).
   - **Therapy Management (CRUD)**: Add new therapies (with image upload/URL, pricing, category, descriptions), edit existing therapies, toggle active/inactive status, and delete therapies.
   - **Appointment Bookings Manager**: View requests, update status (Pending, Confirmed, Completed, Cancelled), direct call/WhatsApp patient.
   - **Admin Security**: Session authentication and password changing.

---

## Getting Started

### 1. Requirements
- Python 3.9+
- Flask (`pip install -r requirements.txt`)

### 2. Running the Server
```bash
python app.py
```
Open your browser and navigate to:
- Public Website: `http://localhost:5000`
- Admin Login: `http://localhost:5000/admin/login`

### Default Admin Credentials:
- **Username**: `admin`
- **Password**: `rahul1234`
*(You can change the password anytime from the Admin Dashboard)*

---

## Contact & Business Details
- **Business Name**: Rahul Physio – Home Visit Physiotherapy
- **Phone**: 7023029646
- **Service Area**: Jaipur, Rajasthan, India
- **Operating Timings**: Morning 6:00 AM – 2:00 PM | Night 9:00 PM – 12:00 AM
