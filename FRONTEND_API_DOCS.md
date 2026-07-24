# 🚀 EDUQASH PRO - Frontend Dasturchi uchun To'liq API Hujjatlari (API Documentation)

Barcha API lar **JSON** formatida ishlaydi. Avtorizatsiya talab qilinadigan endpoint'lar uchun HTTP Header'da `Authorization` kalitini yuborish kerak:
```http
Authorization: Bearer <your_access_token>
```

Swagger UI interfeysi: `http://127.0.0.1:8000/swagger/` yoki `http://127.0.0.1:8000/docs/`

---

## 1. 🔑 Accounts & Auth (`/auth/`)

| Method | Endpoint | Tavsif / Vazifasi | Request Payload / Params | Response |
| :--- | :--- | :--- | :--- | :--- |
| **POST** | `/auth/register/` | Yangi foydalanuvchi ro'yxatdan o'tishi | `{"username", "email", "password", "first_name", "last_name", "role": "student"|"teacher"}` | `{user, tokens: {access, refresh}, message}` |
| **POST** | `/auth/login/` | Tizimga kirish | `{"username", "password"}` yoki `{"email", "password"}` | `{user, tokens: {access, refresh}}` |
| **POST** | `/auth/verify-email/` | Emailga kelgan 6 xonali kodni tasdiqlash | `{"email", "code"}` | `{"message": "Email successfully verified."}` |
| **POST** | `/auth/google/` | Google OAuth orqali avtorizatsiya | `{"email", "google_id", "first_name", "last_name"}` | `{user, tokens}` |
| **POST** | `/auth/telegram/` | Telegram Auth/Bot orqali avtorizatsiya | `{"telegram_id", "first_name", "last_name", "username"}` | `{user, tokens}` |
| **POST** | `/auth/token/refresh/` | Access tokenni yangilash | `{"refresh": "<refresh_token>"}` | `{"access": "<new_access_token>"}` |
| **POST** | `/auth/forgot-password/` | Parolni unutganda emailga kod yuborish | `{"email"}` | `{"message": "Code sent..."}` |
| **POST** | `/auth/reset-password/` | Kodi orqali parolni yangilash | `{"email", "code", "new_password"}` | `{"message": "Password reset successful."}` |
| **POST** | `/auth/change-password/` | Tizimdagi foydalanuvchi parolini o'zgartirishi | `{"old_password", "new_password"}` *(Authed)* | `{"message": "Password updated successfully."}` |
| **GET / PUT / PATCH** | `/auth/profile/` | Profil ma'lumotlarini olish / tahrirlash | `{"first_name", "last_name", "phone", "avatar"}` *(Authed)* | User obyekti ma'lumotlari |

---

## 2. 🏢 Learning Centers (`/centers/`)

| Method | Endpoint | Tavsif / Vazifasi | Params / Payload |
| :--- | :--- | :--- | :--- |
| **GET** | `/centers/` | O'quv markazlari ro'yxati | Filtrlash: `?search=...&owner=<uuid>&ordering=rating` |
| **POST** | `/centers/` | Yangi o'quv markazi yaratish | Payload: `{"name", "description", "address", "phone", "telegram"}` *(Owner/Admin)* |
| **GET / PUT / PATCH / DELETE** | `/centers/{id}/` | Markaz ma'lumotlarini ko'rish / tahrirlash / o'chirish | Object ID |

---

## 3. 📚 Courses, Lessons & Homeworks (`/courses/`)

| Method | Endpoint | Tavsif / Vazifasi | Params / Payload |
| :--- | :--- | :--- | :--- |
| **GET** | `/courses/` | Kurslar ro'yxati | Params: `?type=online|offline&teacher=<uuid>&center=<uuid>&search=...` |
| **POST** | `/courses/` | Yangi kurs yaratish | Payload: `{"title", "description", "price", "type", "center"}` *(Teacher/Admin)* |
| **GET / PUT / PATCH / DELETE** | `/courses/{id}/` | Kursni ko'rish / tahrirlash / o'chirish | Course ID |
| **GET / POST** | `/courses/lessons/` | Darslar ro mezonlari / Qo'shish | Filter: `?course=<course_id>`. POST Payload: `{"course", "title", "video_url", "content"}` |
| **GET / POST** | `/courses/homeworks/` | Uy vazifalari | Filter: `?lesson=<lesson_id>`. POST Payload: `{"lesson", "title", "description", "file"}` |
| **GET / POST** | `/courses/submissions/` | Topshirilgan vazifalar | Filter: `?homework=<id>&student=<id>`. POST Payload: `{"homework", "submission_text", "file"}` |
| **PUT / PATCH** | `/courses/submissions/{id}/` | Vazifani baholash (O'qituvchi) | Payload: `{"score": 90, "teacher_feedback": "Barakalla!"}` |

---

## 4. 📝 Exams & IELTS Band Calculator (`/exams/`)

| Method | Endpoint | Tavsif / Vazifasi | Params / Payload |
| :--- | :--- | :--- | :--- |
| **GET / POST** | `/exams/` | Imtihonlar ro'yxati / Yaratish | Filter: `?exam_type=ielts_mock|cefr|custom`. POST: `{"title", "exam_type", "duration_minutes"}` |
| **POST** | `/exams/{id}/start_attempt/` | Imtihon topshirishni boshlash | *(Authed)* -> Res: `ExamAttempt` obyekti |
| **GET / POST** | `/exams/sections/` | Imtihon bo'limlari (Listening, Reading...) | Filter: `?exam=<exam_id>` |
| **GET / POST** | `/exams/questions/` | Savollar ro'yxati / Qo'shish | Filter: `?section=<section_id>&question_type=multiple_choice|text` |
| **GET** | `/exams/attempts/` | Foydalanuvchining imtihon topshirishlar tarixi | Authed foydalanuvchi tarixi |
| **POST** | `/exams/attempts/{id}/submit/` | Imtihon javoblarini topshirish va IELTS Band hisoblash | Payload: `{"answers": [{"question_id": "...", "selected_choice_id": "...", "text_answer": "..."}]}` -> Avto-baholaydi |

---

## 5. 🧩 Quizzes, Question Banks & Leaderboard (`/quizzes/`)

| Method | Endpoint | Tavsif / Vazifasi | Params / Payload |
| :--- | :--- | :--- | :--- |
| **GET / POST** | `/quizzes/banks/` | Savol banklari ro'yxati / Yaratish | `{"title", "description", "category"}` |
| **GET / POST** | `/quizzes/` | Quizlar ro'yxati / Yaratish | Filter: `?question_bank=<id>&timed=true`. Payload: `{"title", "question_bank", "time_limit_minutes"}` |
| **POST** | `/quizzes/attempts/` | Quiz topshirish va natijani saqlash | Payload: `{"quiz": "<id>", "score": 85, "time_spent_seconds": 120}` -> Leaderboard avto-yangilanadi |
| **GET** | `/quizzes/leaderboard/` | Peshqadamlar jadvali (Reyting) | Filter: `?quiz=<quiz_id>` |
| **POST** | `/quizzes/import-excel/` | Excel (.xlsx) fayldan savollarni yuklash | Form-data: `file: <.xlsx>`, `bank_id: <uuid>` |

---

## 6. 🤖 AI Assistant Services (`/ai/`)

| Method | Endpoint | Tavsif / Vazifasi | Request Payload | Response |
| :--- | :--- | :--- | :--- | :--- |
| **POST** | `/ai/check-essay/` | Inshoni AI bilan tahlil qilish | `{"essay_text": "...", "topic": "..."}` | `{"feedback": "...", "band_prediction": 7.0}` |
| **POST** | `/ai/grammar-fix/` | Matndagi grammatik xatolarni tuzatish | `{"text": "I goes to school yesterday."}` | `{"correction": "I went to school yesterday."}` |
| **POST** | `/ai/roadmap/` | Individual o'quv rejasini tuzish | `{"target_goal": "IELTS 7.5", "current_level": "B1"}` | `{"roadmap": "..."}` |
| **POST** | `/ai/check-homework/` | Uy vazifasini AI bilan avto-tekshirish | `{"homework_description": "...", "submission_text": "..."}` | `{"evaluation": "..."}` |

---

## 7. 💳 Payments & Promo Codes (`/payments/`)

| Method | Endpoint | Tavsif / Vazifasi | Params / Payload |
| :--- | :--- | :--- | :--- |
| **GET** | `/payments/` | To'lovlar tarixi | Authed user o'zinikini, Admin barchasinikini ko'radi |
| **POST** | `/payments/create/` | Yangi to'lov yaratish | Payload: `{"course_id": "...", "amount": 150000, "provider": "payme"|"click"|"fake", "promo_code": "PROMO10"}` |
| **POST** | `/payments/verify/` | Tranzaksiyani tasdiqlash | Payload: `{"transaction_id": "..."}` |
| **POST** | `/payments/apply-promo/` | Promokodni tekshirish va chegirma olish | Payload: `{"code": "PROMO20"}` -> Res: `{"discount_percent": 20}` |
| **GET / POST** | `/payments/promos/` | Promokodlar boshqaruvi (Admin) | `{"code", "discount_percent", "valid_until", "usage_limit"}` |

---

## 8. 🎓 Certificates (`/certificates/`)

| Method | Endpoint | Tavsif / Vazifasi | Params / Payload |
| :--- | :--- | :--- | :--- |
| **GET** | `/certificates/` | Foydalanuvchi sertifikatlari ro'yxati | Authed user sertifikatlari, PDF va QR havolasi bilan |
| **POST** | `/certificates/issue/` | Sertifikat taqdim etish (PDF & QR avto-generatsiya) | Payload: `{"user_id": "...", "course_id": "...", "title": "IELTS Graduation"}` *(Teacher/Admin)* |
| **GET** | `/certificates/verify/{unique_id}/` | Sertifikatni tekshirish (Public QR Verification) | URL parameter: `unique_id` |

---

## 9. 💬 Chat Service (REST & WebSockets)

### REST API:
- `GET /chat/conversations/` — Barcha suhbatlar ro'yxati
- `POST /chat/conversations/` — Yangi suhbat boshlash: `{"participant_ids": ["uuid1", "uuid2"], "title": "Chat"}`
- `GET /chat/messages/?conversation=<uuid>` — Suhbatdagi xabarlar tarixi
- `POST /chat/messages/` — Rasm/Fayl biriktirib xabar yuborish (`file`, `text`, `conversation`)

### WebSocket Real-time:
- **URL**: `ws://127.0.0.1:8000/ws/chat/<conversation_id>/?token=<access_token>`
- **Client -> Server**: `{"message": "Salom"}`
- **Server -> Client**: `{"id": "msg-id", "sender_id": "user-id", "sender_username": "ismat", "message": "Salom", "created_at": "..."}`

---

## 10. ⭐️ Reviews & Reports (`/reviews/`)

| Method | Endpoint | Tavsif / Vazifasi | Params / Payload |
| :--- | :--- | :--- | :--- |
| **GET / POST** | `/reviews/` | Sharhlar ro'yxati / Sharh qoldirish | Filter: `?course=<id>&center=<id>&teacher=<id>&rating=5`. POST: `{"course": "...", "rating": 5, "comment": "Ajoyib kurs"}` |
| **POST** | `/reviews/{id}/like/` | Sharhga like bosish | Object ID |
| **POST** | `/reviews/{id}/dislike/` | Sharhga dislike bosish | Object ID |
| **POST** | `/reviews/reports/` | Nomaqbul sharh ustidan shikoyat qilish | Payload: `{"review": "<id>", "reason": "Beodoblik"}` |

---

## 11. 🔔 Notifications (`/notifications/`)

| Method | Endpoint | Tavsif / Vazifasi | Payload |
| :--- | :--- | :--- | :--- |
| **GET** | `/notifications/` | Foydalanuvchiga kelgan bildirishnomalar ro'yxati | Authed user |
| **POST** | `/notifications/{id}/mark_as_read/` | Bitta bildirishnomani o'qilgan deb belgilash | Object ID |
| **POST** | `/notifications/mark_all_read/` | Barcha bildirishnomalarni o'qilgan deb belgilash | No payload |

---

## 12. 📊 Analytics (`/analytics/`)

| Method | Endpoint | Tavsif / Vazifasi | Authorization |
| :--- | :--- | :--- | :--- |
| **GET** | `/analytics/overview/` | Platformadagi umumiy foydalanuvchilar, kurslar, daromad statistikasi | Admin / SuperAdmin |
| **GET** | `/analytics/revenue/` | To'lovlar usuli va statusi bo'yicha daromad tahlili | Admin / SuperAdmin |
