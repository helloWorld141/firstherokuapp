from django.db import models

# Create your models here.
class Cargo(models.Model):
	id = models.CharField(max_length=50, primary_key=True)
	dims = models.CharField(max_length=255, null=True)
	stackable = models.NullBooleanField(null=True)
	tiltable = models.NullBooleanField(null=True)
	image = models.ImageField()
	crops = models.CharField(max_length=255)
	pieces = models.CharField(max_length=255, null=True)
	type =models.CharField(max_length=255, default="CUBOID")
