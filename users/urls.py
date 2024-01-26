from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  home
router = DefaultRouter()
from .views import RegistrationView, ConfirmationView, LoginView, LogoutView, home, request_blood, activate,UserRegistrationApiView, UserListView, UserLogoutView, UserLoginApiView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
# router.register('list', UserListView)
urlpatterns = [
    # path('', include(router.urls)),
    path('', home, name="home"),
    path('request-blood/<int:user_id>/', request_blood, name='request_blood'),
    path('register/', UserRegistrationApiView.as_view(), name='register'),
    path('confirm/<str:uid>/<str:token>/', ConfirmationView.as_view(), name='confirm'),
    path('login/', LoginView.as_view(), name='login'),
    path('login1/', UserLoginApiView.as_view(), name='login1'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout1/', UserLogoutView.as_view(), name='logout1'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('active/<uid64>/<token>/', activate, name = 'activate'),
]