from django.contrib import admin

# Register your models here.
from .models import Profile, TherapistProfile, ClientProfile

admin.site.register(Profile)
admin.site.register(TherapistProfile)
admin.site.register(ClientProfile)
