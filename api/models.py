from django.db import models

# Create your models here.
class Cargo(models.Model):
	id = models.CharField(max_length=50, primary_key=True)
	dims = models.CharField(max_length=255)
	stackable = models.NullBooleanField(null=True)
	tiltable = models.NullBooleanField(null=True)
	image = models.ImageField()
	crops = models.CharField(max_length=255)
	pieces = models.IntegerField(null=True)
