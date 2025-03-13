from django.db import models
import django.utils.timezone as timezone

# Create your models here.

class Form(models.Model):
	
	guide_name = models.CharField(max_length=255)
	designation = models.CharField(max_length=255)
	department = models.CharField(max_length=255)
	mobile_number = models.CharField(max_length=20)
	email = models.EmailField()
	institution_address = models.TextField()
	
	def __str__(self):
		return self.guide_name

class SignupOTP(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Signup OTP for {self.email}: {self.code}"

class PendingSignup(models.Model):
    email = models.EmailField(unique=True)
    details = models.TextField()  # stores the signup request details (as a string)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PendingSignup: {self.email}"
