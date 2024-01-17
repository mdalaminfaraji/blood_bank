from django.contrib import admin
from .models import DonationEvent, DonationHistory,UserDetails
# Register your models here.
admin.site.register(UserDetails)
admin.site.register(DonationEvent)
admin.site.register(DonationHistory)