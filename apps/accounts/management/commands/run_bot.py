import os
import sys
import time
import requests

# Direct execution path setup
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../../../../'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import django
from django.apps import apps
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
if not apps.ready:
    django.setup()

from django.core.management.base import BaseCommand
from django.conf import settings
from apps.accounts.models import User


class Command(BaseCommand):
    help = "Telegram Botni Polling rejimida ishga tushirish (/start buyrug'ini qabul qilish va foydalanuvchini ulash)"

    def handle(self, *args, **options):
        bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
        if not bot_token or bot_token == 'your_telegram_bot_token_here':
            self.stderr.write(self.style.ERROR("Xatolik: TELEGRAM_BOT_TOKEN .env faylida kiritilmagan yoki noto'g'ri!"))
            return

        self.stdout.write(self.style.SUCCESS("Telegram Bot muvaffaqiyatli ishga tushdi! Xabarlar kutilmoqda... (To'xtatish uchun Ctrl+C)"))
        offset = 0

        while True:
            try:
                url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
                response = requests.get(url, params={'offset': offset, 'timeout': 10})
                data = response.json()

                if data.get('ok'):
                    for update in data.get('result', []):
                        offset = update['update_id'] + 1
                        message = update.get('message')
                        if not message:
                            continue

                        chat = message.get('chat', {})
                        chat_id = str(chat.get('id'))
                        text = message.get('text', '')
                        first_name = chat.get('first_name', '')
                        last_name = chat.get('last_name', '')
                        username = chat.get('username', '')

                        if text.startswith('/start'):
                            # Foydalanuvchini izlash yoki yangi hisob yaratish
                            user = User.objects.filter(telegram_id=chat_id).first()
                            if not user:
                                uname = username or f"tg_{chat_id}"
                                user = User.objects.create_user(
                                    username=uname,
                                    first_name=first_name,
                                    last_name=last_name,
                                    telegram_id=chat_id,
                                    is_email_verified=True
                                )
                                reply_text = (
                                    f"<b>Assalomu alaykum, {first_name}!</b>\n\n"
                                    f"Siz EDUQASH PRO tizimiga muvaffaqiyatli ulandingiz!\n"
                                    f"Sizning Telegram ID: <code>{chat_id}</code>\n\n"
                                    f"Endi platformadagi bildirishnomalar va xabarlarni ushbu bot orqali qabul qilasiz."
                                )
                            else:
                                reply_text = (
                                    f"<b>Qaytganingiz bilan, {user.first_name or user.username}!</b>\n\n"
                                    f"Sizning Telegram hisobingiz tizimga ulangan.\n"
                                    f"Telegram ID: <code>{chat_id}</code>"
                                )

                            # Telegram'ga javob yuborish
                            send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                            requests.post(send_url, json={
                                'chat_id': chat_id,
                                'text': reply_text,
                                'parse_mode': 'HTML'
                            })
                            self.stdout.write(self.style.SUCCESS(f"[GET /start] Foydalanuvchi: {first_name} (ID: {chat_id})"))

            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING("\nBot to'xtatildi."))
                break
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Xatolik yuz berdi: {e}"))
                time.sleep(3)


if __name__ == '__main__':
    import os
    import sys
    import django

    # Loyiha ildiz papkasini (eduqash2) sys.path ga qo'shish
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../../../../'))
    if ROOT_DIR not in sys.path:
        sys.path.insert(0, ROOT_DIR)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

    cmd = Command()
    cmd.handle()

