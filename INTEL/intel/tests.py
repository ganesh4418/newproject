from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.test import TestCase
from rest_framework import status
from .models import RequestDemo, Contact, HelpandSupport, UserProfile
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
import os


class AuthenticationTest(APITestCase):
    def test_user_signup(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example.com',
        }
        response = self.client.post('/api/signup/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        User = get_user_model()
        user = User.objects.create_user('testuser', password='testpassword')
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_with_incorrect_credentials(self):
        User = get_user_model()
        user = User.objects.create_user('testuser', password='testpassword')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        response = self.client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class RequestDemoTestCase(TestCase):
    def setUp(self):
        # Create a sample RequestDemo object for testing
        self.demo = RequestDemo.objects.create(
            Full_name="John Doe",
            Company="Example Company",
            Business_email="john@example.com",
            Contact_number="1234567890"
        )

    def test_request_demo_model_str(self):
        # Test the __str__ method of the RequestDemo model
        self.assertEqual(str(self.demo), "John Doe")

    def test_request_demo_fields(self):
        # Test individual fields of the RequestDemo model
        self.assertEqual(self.demo.Full_name, "John Doe")
        self.assertEqual(self.demo.Company, "Example Company")
        self.assertEqual(self.demo.Business_email, "john@example.com")
        self.assertEqual(self.demo.Contact_number, "1234567890")

    def test_request_demo_email_field(self):
        # Test the Business_email field using an invalid email
        # Swith self.assertRaises(ValueError):
            RequestDemo.objects.create(
                Full_name="Jane Smith",
                Company="Another Company",
                Business_email="invalid-email",  # Invalid email address
                Contact_number="9876543210"
            )

class ContactTestCase(TestCase):
    def setUp(self):
        # Create a sample RequestDemo object for testing
        self.demo = Contact.objects.create(
            Full_name="John Doe",
            Company="Example Company",
            Business_email="john@example.com",
            Contact_number="1234567890"
        )

    def test_Contact_model_str(self):
        # Test the str method of the RequestDemo model
        self.assertEqual(str(self.demo), "John Doe")

    def test_Contact_fields(self):
        # Test individual fields of the RequestDemo model
        self.assertEqual(self.demo.Full_name, "John Doe")
        self.assertEqual(self.demo.Company, "Example Company")
        self.assertEqual(self.demo.Business_email, "john@example.com")
        self.assertEqual(self.demo.Contact_number, "1234567890")

    def test_Contact_email_field(self):
        # Test the Business_email field using an invalid email
        # Swith self.assertRaises(ValueError):
            Contact.objects.create(
                Full_name="Jane Smith",
                Company="Another Company",
                Business_email="invalid-email",  # Invalid email address
                Contact_number="9876543210"
            )

class HelpandSupportTestCase(TestCase):
    def setUp(self):
        # Create a sample RequestDemo object for testing
        self.demo = HelpandSupport.objects.create(
            Full_name="John Doe",
            Company="Example Company",
            Business_email="john@example.com",
            Contact_number="1234567890"
        )

    def test_Help_and_Support_model_str(self):
        # Test the str method of the RequestDemo model
        self.assertEqual(str(self.demo), "John Doe")

    def test_Help_and_Support_fields(self):
        # Test individual fields of the RequestDemo model
        self.assertEqual(self.demo.Full_name, "John Doe")
        self.assertEqual(self.demo.Company, "Example Company")
        self.assertEqual(self.demo.Business_email, "john@example.com")
        self.assertEqual(self.demo.Contact_number, "1234567890")

    def test_Help_and_Support_email_field(self):
        # Test the Business_email field using an invalid email
        # Swith self.assertRaises(ValueError):
            HelpandSupport.objects.create(
                Full_name="Jane Smith",
                Company="Another Company",
                Business_email="invalid-email",  # Invalid email address
                Contact_number="9876543210"
            )

class UserProfileTestCase(TestCase):
    def setUp(self):
        # Create a sample image file for testing
        self.image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")

    def test_create_user_profile(self):
        # Create a UserProfile instance
        user_profile = UserProfile.objects.create(profile_photo=self.image)

        # Verify that the instance was created correctly
        self.assertIsInstance(user_profile, UserProfile)

    def test_profile_photo_upload_path(self):
        # Ensure that the profile_photo field uploads to the correct path
        user_profile = UserProfile(profile_photo=self.image)
        upload_to = user_profile._meta.get_field('profile_photo').upload_to

        # Normalize the paths for comparison
        normalized_upload_to = os.path.normpath(upload_to)
        normalized_expected_path = os.path.normpath('profile-photos')

        self.assertEqual(normalized_upload_to, normalized_expected_path)

    def test_image_upload(self):
        # Check if the image was uploaded successfully
        user_profile = UserProfile(profile_photo=self.image)
        uploaded_image_path = user_profile.profile_photo.path

    def test_delete_user_profile(self):
        # Delete a UserProfile instance and ensure it is removed from the database
        user_profile = UserProfile.objects.create(profile_photo=self.image)
        user_profile_id = user_profile.id
        user_profile.delete()
        self.assertIsNone(UserProfile.objects.filter(id=user_profile_id).first())