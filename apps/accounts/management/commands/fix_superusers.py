from django.core.management.base import BaseCommand
from apps.accounts.models import User


class Command(BaseCommand):
    help = "Barcha superuser (is_superuser=True) foydalanuvchilarning rolini super_admin va approved holatiga o'tkazish"

    def handle(self, *args, **options):
        superusers = User.objects.filter(is_superuser=True)
        count = 0
        for user in superusers:
            user.role = 'super_admin'
            user.role_approval_status = 'approved'
            user.is_email_verified = True
            user.save()
            count += 1
            self.stdout.write(self.style.SUCCESS(f"Foydalanuvchi {user.username} -> super_admin qilib yangilandi."))

        self.stdout.write(self.style.SUCCESS(f"Jami {count} ta superuser muvaffaqiyatli yangilandi."))
