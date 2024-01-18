# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserDetails, DonationEvent, DonationHistory
from .forms import UserDetailsForm, DonationEventForm




@login_required
def user_Details(request):
    if request.method=='POST':
        form=UserDetailsForm(request.POST)
        if form.is_valid():
            user_Details=form.save(commit=False)
            user_Details.user=request.user
            user_Details.save()
            messages.success(request, 'User details updated successfully.')
            return redirect('user_dashboard')
    else:
        form=UserDetailsForm()
        return render(request, "user_profile_details.html", {"form":form})
    
@login_required
def update_userdetails(request, pk):
    user_details = get_object_or_404(UserDetails, pk=pk, user=request.user)

    if request.method == 'POST':
        form = UserDetailsForm(request.POST, instance=user_details)
        if form.is_valid():
            form.save()
            return redirect('success_url_name')  # Change 'success_url_name' to the actual URL name for success
    else:
        form = UserDetailsForm(instance=user_details)

    return render(request, 'userdetails_form.html', {'form': form})    
@login_required
def donation_event_list(request):
    events = DonationEvent.objects.exclude(creator=request.user)
    return render(request, 'donation_event_list.html', {'events': events})


@login_required
def create_donation_event(request):
    if request.method == 'POST':
        form = DonationEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            messages.success(request, "Your Request is successfully create")
            return redirect('home')
    else:
        form = DonationEventForm()

    return render(request, 'create_donation_event.html', {'form': form})


@login_required
def accept_donation_event(request, event_id):
    event = get_object_or_404(DonationEvent, id=event_id)

    if request.method == 'POST':
        # Assuming the current user is accepting the event
        event.acceptors.add(request.user)
        event.is_get_blood=True
        event.save()
        # Create a DonationHistory entry
        DonationHistory.objects.create(
            donor=event.creator,
            recipient=request.user,
            event=event,
            successful=True # Set to True when the donation is successful
        )
        messages.success(request, f"You have accepted the donation request for {event.creator.username}.")
        return redirect('home')

    return render(request, 'accept_donation_event.html', {'event': event})

@login_required
def user_dashboard(request):
    donation_events = DonationEvent.objects.exclude(creator=request.user, is_get_blood=True)
    donation_history = DonationHistory.objects.filter(donor=request.user)


    return render(request, 'user_dashboard.html', {
        'donation_events': donation_events,
        'donation_history': donation_history,
    })

@login_required
def blood_requests(request):
    donation_events = DonationEvent.objects.exclude(creator=request.user, is_get_blood=True)
    return render(request, 'blood_requests.html', {'donation_events': donation_events})

@login_required
def accept_request(request, event_id):
    event = get_object_or_404(DonationEvent, pk=event_id)

    # Check if the user has already accepted the event
    if request.user not in event.acceptors.all():
        event.acceptors.add(request.user)
        event.is_get_blood=True
        event.save()
        DonationHistory.objects.create(donor=request.user, recipient=event.creator, event=event, successful=True)

    return redirect('home')

@login_required
def donation_history(request):
    donation_history = DonationHistory.objects.filter(donor=request.user)
    return render(request, 'donation_history.html', {'donation_history': donation_history})


