from django.views import View
from django.shortcuts import render, redirect
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
def home(request):
    return render(request, "home.html")

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
            confirm_link = f"http://127.0.0.1:8000/confirm/{uid}/{token}"

            # Email subject and body
            email_subject = "Confirm Your Registration"
            email_body = render_to_string('confirmation_email.html', {'confirm_link': confirm_link})
            email=EmailMultiAlternatives(email_subject, "", to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()


            return redirect('login')

        return render(request, self.template_name, {'form': form})

    
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
