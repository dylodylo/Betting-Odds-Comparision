from django.db import models
# Create your models here.

class Match(models.Model):
	username = models.CharField(max_length=100)