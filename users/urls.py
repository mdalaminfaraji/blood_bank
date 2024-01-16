from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  home
router = DefaultRouter()
from .views import RegistrationView, ConfirmationView, LoginView, LogoutView, home



urlpatterns = [
    path('', home, name="home"),
    path('register/', RegistrationView.as_view(), name='register'),
    path('confirm/<str:uid>/<str:token>/', ConfirmationView.as_view(), name='confirm'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]