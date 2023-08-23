from django.urls import path
from .views import *



urlpatterns = [
    path('registation_api/',UserRegistration.as_view(),name='registration_api'),
    path('login/',UserLogin.as_view(),name='login'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('change_password/',ChangePassword.as_view(),name='change_password')
    

]
