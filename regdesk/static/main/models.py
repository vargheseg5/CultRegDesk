from django.db import models
from django.contrib.auth.models import User

class Participent(models.Model):
	name = models.CharField(max_length = 50)
	institution = models.CharField(max_length = 100)
	email = models.EmailField(null = True)
	phone_no = models.BigIntegerField(null = True)
	gender = models.CharField(max_length = 1)
	dob = models.DateField(auto_now=False, auto_now_add=False)

class Event(models.Model):
	name = models.CharField(max_length = 150)
	minimum = models.IntegerField(null = True)
	maximum = models.IntegerField(null = True)
	fee = models.IntegerField(null = True)
	team = models.NullBooleanField()

class Registration(models.Model):
	event = models.OneToOneField(Event)
	user = models.OneToOneField(User)

class Participation(models.Model):
	participent = models.OneToOneField(Participent)
	registration = models.OneToOneField(Registration)

class User_detail(models.Model):
	section = models.CharField(max_length = 5)
	phone_no = models.BigIntegerField(null = True)
	user = models.OneToOneField(User)