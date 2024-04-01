
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include 
from . import views  
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView,PasswordResetCompleteView

urlpatterns = [
  path("signup/", views.signup, name="signup"),
  path("logout/", views.mylogout, name="logout"), 
  path("login/", views.mylogin, name="login"),
  path("profile_edit", views.profileEdit, name="profileEdit"), 
  path("view_profile/", views.viewProfile,name="profile_view" ),
  path('password_reset/', views.ResetPasswordView.as_view(),name="password_reset"), 
  path('password_reset/done/',PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
       name="password_reset_done"),
   path('password-reset-confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'),
         name='password_reset_confirm'), 
  path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),
  path("signup/check_username/", views.check_username, name="check_username"),
   path("signup/check_email/", views.check_email, name="check_email"),
   path("signup/check_password/",views.check_password,name="check_password"), 
   
]
