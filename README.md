# EDUQASH PRO V2.0 - Production Ready Django Backend

EDUQASH PRO V2.0 is a complete, scalable, zero-paid-service backend built with Python 3.11, Django 5.0, Django REST Framework, Django Channels (WebSockets), Celery, PostgreSQL, and Redis.

## Features & Highlights

1. **Zero Paid Services Architecture**:
   - **Email Verification**: Built-in OTP email verification via SMTP (No paid SMS service).
   - **Free AI Providers**: Switchable AI Service using **MegaLLM.uz** or **Groq API** (`AI_PROVIDER=groq` / `AI_PROVIDER=megallm`).
   - **OpenStreetMap**: Geographic latitude and longitude stored natively without paid Google Maps APIs.
   - **Local Storage**: Django `FileSystemStorage` configured in `/media/` (No S3 costs).
   - **PostgreSQL Full-Text Search**: Native PostgreSQL full-text search capability.
   - **Free Notifications**: Email (SMTP) + Telegram Bot API dispatcher + Firebase FCM ready.
   - **Zero-Fee Payments**: `FAKE_PAYMENT=True` instant approval mode for development without gateway fees.
   - **Free Certificate Engine**: PDF generation using `reportlab` and QR Code verification using `qrcode[pil]`.
   - **Excel Import**: Excel bulk quiz import using `openpyxl`.

2. **Core App Architecture**:
   - **`accounts`**: Custom `User` model (`super_admin`, `admin`, `moderator`, `teacher`, `center_owner`, `student`), JWT Authentication (Register, Login, Email Verify, Google, Telegram, Password Reset).
   - **`centers`**: Learning Center management with search, filters, geolocation coordinates, ratings, and owner permissions.
   - **`courses`**: Course (Online/Offline/Hybrid), Lessons, Video/PDF materials, Homework & Homework Submissions with scoring & feedback.
   - **`exams`**: Unified engine for IELTS (Listening, Reading, Writing, Speaking), SAT (Math, Reading), and CEFR (A1-C2). Built-in automated Band Score Calculators.
   - **`quizzes`**: Question Bank, Quiz attempts, timed tests, Leaderboards, Excel bulk question importer (`POST /quizzes/import-excel/`).
   - **`ai_assistant`**: AI essay evaluation, IELTS writing band predictor, grammar correction, homework checker, and personalized learning roadmap generator.
   - **`payments`**: Payment processing (Payme/Click/Uzum/Fake), transaction verification, promo codes/coupons system.
   - **`certificates`**: Dynamic PDF certificate generator with embedded verification QR code and public verification API (`/certificates/verify/<unique_id>/`).
   - **`chat`**: Real-time WebSocket chat (`ws://localhost:8000/ws/chat/<conversation_id>/`) powered by Django Channels + Redis with JWT authentication middleware.
   - **`reviews`**: Ratings, comments, like/dislike counts, and review moderation reporting.
   - **`notifications`**: Dual-channel notification system (Email + Telegram Bot API).
   - **`analytics`**: Platform stats dashboard, revenue tracking (daily/weekly/monthly), student enrollments, exam completion statistics.

---

## Installation & Setup Guide

### 1. Environment Setup
Ensure Python 3.11+ and Redis are installed on your machine.

```bash
# Clone or navigate to project directory
cd eduqash2

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Ensure `.env` contains your PostgreSQL DB credentials, Redis URL, AI Provider keys, and Telegram Bot details:

```ini
SECRET_KEY=django-insecure-eduqash-pro-v2-super-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

DB_NAME=eduqash_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1

AI_PROVIDER=groq
MEGALLM_API_URL=https://api.megallm.uz/v1
MEGALLM_API_KEY=your_megallm_key
GROQ_API_KEY=your_groq_key

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
FAKE_PAYMENT=True
```

### 3. Database Migration & Superuser

```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser admin
python manage.py createsuperuser
```

### 4. Running Development Server (HTTP + WebSockets)

```bash
# Run server using Daphne (ASGI) or standard manage.py
python manage.py runserver
```

### 5. Running Celery Worker (Background tasks for Emails)

```bash
celery -A config worker -l info
```

---

## Interactive API Documentation (Swagger / OpenAPI 3)

Access interactive Swagger UI and Redoc documentation at:

- **Swagger UI**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/) or [http://localhost:8000/docs/](http://localhost:8000/docs/)
- **Redoc**: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)
- **OpenAPI Schema**: [http://localhost:8000/schema/](http://localhost:8000/schema/)

---

## WebSocket Chat Protocol

- **Endpoint**: `ws://localhost:8000/ws/chat/<conversation_id>/?token=<JWT_ACCESS_TOKEN>`
- Send Payload: `{"message": "Hello world!"}`
- Receive Event: `{"type": "chat_message", "id": "...", "sender_id": "...", "sender_username": "...", "message": "Hello world!", "created_at": "..."}`
