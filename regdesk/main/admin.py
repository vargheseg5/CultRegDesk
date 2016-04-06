from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Participent, Event, Participation, Registration, User_detail

class ModelUserDetails(admin.StackedInline):
	model = User_detail
	can_delete = False
	verbose_name_plural = 'User details'

class ModelRegistration(admin.StackedInline):
	model = Registration
	can_delete = True
	verbose_name_plural = 'Registrations'

class UserAdmin(UserAdmin):
	inlines = [ModelUserDetails, ModelRegistration]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Participent)
admin.site.register(Event)
admin.site.register(Participation)