from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm 
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authtoken.models import Token
from django.db.models import Q
from blood.models import DonationEvent
from blood.models import UserDetails, DonationHistory
from blood.forms import DonationEventForm
from django.utils import timezone

from django.contrib import messages
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistrationSerializer, UserLoginSerializer
from rest_framework.views import APIView

from django.contrib.auth.models import User
from .serializers import UserSerializer
def success_response(data=None, message="Success", code=status.HTTP_200_OK):
    return Response({
        "appStatus": True,
        "appCode": code,
        "appMessage": message,
        "data": data
    }, status=code)

def error_response(errors=None, message="Error", code=status.HTTP_400_BAD_REQUEST):
    return Response({
        "appStatus": False,
        "appCode": code,
        "appMessage": message,
        "errors": errors
    }, status=code)

# class UserListView(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        try:
            # Retrieve the list of users
            users = self.get_queryset()
            serializer = self.get_serializer(users, many=True)

            # Return success response
            return success_response(data=serializer.data, message="Users retrieved successfully", code=200)
        
        except Exception as e:
            # Return error response if an exception occurs
            return error_response(errors=str(e), message="Error retrieving users", code=500)    
    
class UserRegistrationApiView(APIView):
    serializer_class = RegistrationSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"http://127.0.0.1:8000/confirm/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirmation_email.html', {'confirm_link' : confirm_link})
            
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            # Return success response
            return success_response(data="Check your mail for confirmation", message="Registration successful", code=status.HTTP_201_CREATED)
        
        # Return error response if validation fails
        return error_response(errors=serializer.errors, message="Validation failed", code=status.HTTP_400_BAD_REQUEST)

  
def activate(request, uid64, token):
    try: # Error handling kortechi. uid, user nao thakte pare tar mane sekhan theke error asar somvabona ache
    # sejonne code ke try er moddhe rakhlam
        uid = urlsafe_base64_decode(uid64).decode() # encode kora sei uid ke decode kortechi
        user = User._default_manager.get(pk=uid) # decode er por je uid pelam seta kon 
        # user er seta janar jonne ei code ta
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login1')
    else:
        return redirect('register')
    
class UserLoginApiView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data = self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username= username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                print(token)
                print(_)
                login(request, user)
                return Response({'appStatus':True, 'appCode':200, 'appMessage':'Login successful', 'token' : token.key, 'user_id' : user.id}, status=status.HTTP_200_OK)
            else:
                # Return error response for invalid credentials
                return Response({
                    'appStatus': False,
                    'appCode': 401,
                    'appMessage': 'Invalid credentials',
                    'error': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
        return Response({
            'appStatus': False,
            'appCode': 400,
            'appMessage': 'Validation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
class UserLogoutView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)

            # Return success response
            return Response({
                'appStatus': True,
                'appCode': 200,
                'appMessage': 'Logout successful'
            }, status=status.HTTP_200_OK)
        else:
            # Return error response if the user is not authenticated
            return Response({
                'appStatus': False,
                'appCode': 401,
                'appMessage': 'User not authenticated',
                'error': 'User not authenticated'
            }, status=status.HTTP_401_UNAUTHORIZED)

def home(request):
    blood_group_filter = request.GET.get('blood_group', '')
    search_query = request.GET.get('search', '')
    available_donors = UserDetails.objects.filter(availability_for_donation=True)
    donation_events = DonationEvent.objects.all()

    if blood_group_filter:
        donation_events = donation_events.filter(bloodgroup=blood_group_filter)
        available_donors=available_donors.filter(bloodgroup=blood_group_filter)

    if search_query:
        donation_events = donation_events.filter(
            Q(bloodgroup__icontains=search_query) |
            Q(details__icontains=search_query) |
            Q(creator__username__icontains=search_query)
        )    
        available_donors = available_donors.filter(
            Q(bloodgroup__icontains=search_query) 
        )    
    return render(request, "home.html",  {'donation_events': donation_events, 'blood_group_filter': blood_group_filter, 'search_query': search_query, 'available_donors': available_donors})

class RegistrationView(View):
    template_name = 'registration.html'
    form_class = UserRegistrationForm  # Specify your custom form

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save the user to the database yet
            user.is_active = False  # Set is_active to False initially
            user.save()
            # Generate confirmation token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Construct confirmation link
            confirm_link = f"https://blood-bank-z8ix.onrender.com/confirm/{uid}/{token}"

            # Email subject and body
            email_subject = "Confirm Your Registration"
            email_body = render_to_string('confirmation_email.html', {'confirm_link': confirm_link})
            email=EmailMultiAlternatives(email_subject, "", to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()


            return redirect('login')

        return render(request, self.template_name, {'form': form})
    
    
@login_required
def request_blood(request, user_id):
    donor = get_object_or_404(UserDetails, user__id=user_id, availability_for_donation=True)
    if request.method == 'POST':
        donor.availability_for_donation = False
        donor.last_donation_date = timezone.now()
        donor.save()
        
        DonationHistory.objects.create(
        donor=request.user,
        recipient=donor.user,
        donation_date=timezone.now(),
        successful=True
        )
        messages.success(request, 'Your blood request was successful! Thank you for your contribution.')

        return redirect('home')

    return render(request, 'request_blood_details.html', {'donor': donor})
    
class ConfirmationView(View):
    template_name = 'confirmation_email.html'
    redirect_url = 'login' 
    def get(self, request, uid, token):
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User._default_manager.get(pk=uid)
        except User.DoesNotExist:
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect(self.redirect_url)
        else:
            return render(request, self.template_name, {'success': False})

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            print(user)

            if user:
                login(request, user)
                return redirect('home')  # Redirect to the home page or any other page you want
            else:
                return render(request, self.template_name, {'form': form, 'error': 'Invalid credentials'})

        return render(request, self.template_name, {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')       
