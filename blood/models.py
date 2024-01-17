# models.py

from django.contrib.auth.models import User
from django.db import models

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField()
    address = models.TextField()
    last_donation_date = models.DateField(null=True, blank=True)
    availability_for_donation = models.BooleanField(default=True)
    bloodgroup = models.CharField(max_length=5, choices=[('O+', 'O+'), ('O-', 'O-'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-')])

    def __str__(self):
        return self.user.username

class DonationEvent(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    bloodgroup = models.CharField(max_length=5, null=True, blank=True, choices=[('O+', 'O+'), ('O-', 'O-'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-')])
    details = models.TextField(null=True, blank=True)
    acceptors = models.ManyToManyField(User, related_name='accepted_events', blank=True)
    is_get_blood= models.BooleanField(default=False, blank=True)

class DonationHistory(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations_made')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations_received')
    event = models.ForeignKey(DonationEvent, on_delete=models.CASCADE,null=True, blank=True)
    donation_date = models.DateTimeField(auto_now_add=True)
    canceled = models.BooleanField(default=False)
    successful = models.BooleanField(default=False)

    def __str__(self):
        return f'Donation from {self.donor.username} to {self.recipient.username} on {self.donation_date}'

