from django.test import TestCase
from apps.accounts.serializers import RegisterSerializer
from apps.accounts.models import User


class RegistrationTestCase(TestCase):
    def test_admin_registration_allowed(self):
        data = {
            "username": "admin_test",
            "email": "admin_test@gmail.com",
            "password": "password123",
            "first_name": "Admin",
            "last_name": "Test",
            "role": "admin",
            "phone": "+998912630977",
            "bio": "Admin bio"
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.role, "admin")
        self.assertEqual(user.role_approval_status, "pending")

    def test_moderator_registration_allowed(self):
        data = {
            "username": "moderator_test",
            "email": "moderator_test@gmail.com",
            "password": "password123",
            "first_name": "Moderator",
            "last_name": "Test",
            "role": "moderator",
            "phone": "+998912630977",
            "bio": "Moderator bio"
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.role, "moderator")
        self.assertEqual(user.role_approval_status, "pending")

    def test_super_admin_registration_rejected(self):
        data = {
            "username": "super_test",
            "email": "super_test@gmail.com",
            "password": "password123",
            "first_name": "Super",
            "last_name": "Admin",
            "role": "super_admin"
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("role", serializer.errors)
