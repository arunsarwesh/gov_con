from django.db import models

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
