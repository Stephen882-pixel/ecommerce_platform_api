from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import uuid
import json


def get_default_expires_at():
    return timezone.now() + timedelta(hours=1)


# Create your models here.
class PasswordResetRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    old_password = models.CharField(max_length=128, null=True)
    new_password = models.CharField(max_length=128, null=True)
    expires_at = models.DateTimeField(default=get_default_expires_at)

    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"Password change for {self.user.username} - {self.token}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    national_id = models.CharField(max_length=20,blank=True,null=True,unique=True)
    profile_image = models.ImageField(upload_to="profiles/",blank=True,null=True)
    date_of_birth = models.DateField(blank=True,null=True)
    gender = models.CharField(max_length=10,blank=True,null=True,choices=[
        ("male","Male"),
        ("female","Female"),
        ("other","Other")
    ])
    phone_number = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.user.username



class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **Kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **Kwargs)

    def is_valid(self):
        return timezone.now() <= self.expires_at


class PasswordResetSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.ForeignKey(OTP, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    def is_valid(self):
        return not self.is_used and timezone.now() <= self.expires_at


class Address(models.Model):
    ADDRESS_TYPES = [
        ('billing','Billing'),
        ('shipping','Shipping'),
        ('both','Both')
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='addresses')
    address_type = models.CharField(max_length=10,choices=ADDRESS_TYPES)

    # Location details
    country = models.CharField(max_length=100,default="Kenya")
    county = models.CharField(max_length=100)
    constituency = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    estate = models.CharField(max_length=100,blank=True,null=True)
    street = models.CharField(max_length=100,blank=True,null=True)
    landmark = models.CharField(max_length=255,blank=True,null=True)
    postal_code = models.CharField(max_length=55,blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.town}"


