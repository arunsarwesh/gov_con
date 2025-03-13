from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    college_name = models.CharField(max_length=500)
    role = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)

    # Override groups with a custom related_name.
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Custom reverse accessor
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups"
    )
    
    # Override user_permissions with a custom related_name.
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  # Custom reverse accessor
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions"
    )


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
	name = models.CharField(max_length=255)
	College_Name = models.CharField(max_length=500)
	role = models.CharField(max_length=50)
	phone = models.CharField(max_length=20)
	created_at = models.DateTimeField(auto_now_add=True)
	is_approved = models.BooleanField(default=False)
	approved_at = models.DateTimeField(null=True, blank=True)
	
	def __str__(self):
		return f"PendingSignup: {self.email}"
