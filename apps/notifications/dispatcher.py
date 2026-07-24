import requests
from django.core.mail import send_mail
from django.conf import settings
from apps.notifications.models import Notification


class NotificationDispatcher:
    @staticmethod
    def send_notification(user, title, body, notification_type='system', send_email=True, send_telegram=True):
        # 1. Create DB Notification
        notification = Notification.objects.create(
            user=user,
            title=title,
            body=body,
            type=notification_type
        )

        # 2. Send Email if requested & email exists
        if send_email and user.email:
            try:
                send_mail(
                    subject=f"EDUQASH PRO: {title}",
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=True
                )
            except Exception:
                pass

        # 3. Send Telegram message if telegram_id exists & bot token configured
        bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
        if send_telegram and user.telegram_id and bot_token:
            try:
                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                payload = {
                    "chat_id": user.telegram_id,
                    "text": f"<b>{title}</b>\n\n{body}",
                    "parse_mode": "HTML"
                }
                requests.post(url, json=payload, timeout=5)
            except Exception:
                pass

        return notification
