# forms.py
from django import forms
from .models import UserDetails, DonationEvent

class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        fields = ['name', 'age', 'address', 'last_donation_date', 'availability_for_donation', 'bloodgroup']

class DonationEventForm(forms.ModelForm):
    class Meta:
        model = DonationEvent
        fields = ['bloodgroup', 'details']
        

