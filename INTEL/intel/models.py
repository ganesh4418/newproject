from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from django.db import models



class CustomUser(AbstractUser):
    email = models.EmailField()

    def _create_user(self, email, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)

        with transaction.atomic(using=self._db):
            user = self.model(username=username, email=email, **extra_fields)
            if password is not None:
                user.set_password(password)
            else:
                user.set_unusable_password()
            user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self._create_user(username, email, password, **extra_fields)


class RequestDemo(models.Model):
    Full_name = models.CharField(max_length=100)
    Company = models.CharField(max_length=100)
    Business_email = models.EmailField()
    Contact_number = models.CharField(max_length=20)

    def __str__(self):
        return self.Full_name


class Contact(models.Model):
    Full_name = models.CharField(max_length=100)
    Company = models.CharField(max_length=100)
    Business_email = models.EmailField()
    Contact_number = models.CharField(max_length=20)

    def __str__(self):
        return self.Full_name



class HelpandSupport(models.Model):
    Full_name = models.CharField(max_length=100)
    Company = models.CharField(max_length=100)
    Business_email = models.EmailField()
    Contact_number = models.CharField(max_length=20)

    def __str__(self):
        return self.Full_name

class UserProfile(models.Model):
    profile_photo = models.ImageField(upload_to='profile-photos/')

