# urls.py
from django.urls import path
from .views import user_dashboard, blood_requests, accept_request, donation_history, user_Details, create_donation_event,update_userdetails,accept_donation_event, donation_event_list

urlpatterns = [
    path('userdetails/create/', user_Details, name='create_userdetails'),
    path('userdetails/update/<int:pk>/', update_userdetails, name='update_userdetails'),
    path('create/', create_donation_event, name='create_donation_event'),
    path('events/', donation_event_list, name='donation_event_list'),
    path('accept/<int:event_id>/', accept_donation_event, name='accept_donation_event'),
    path('user-dashboard/', user_dashboard, name='user_dashboard'),
    path('blood-requests/', blood_requests, name='blood_requests'),
    path('accept-request/<int:event_id>/', accept_request, name='accept_request'),
    path('donation-history/', donation_history, name='donation_history'),
    # Add other URLs as needed
]
