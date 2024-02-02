from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Custom_login.as_view(), name='login'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path("verify-email/<slug:username>", views.Verify_email.as_view(), name="verify-email"),
    path("resend-otp", views.ResendOtp.as_view(), name="resend-otp"),
    path('logout/', views.Logoutuser.as_view(), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html',html_email_template_name='users/password_reset_email.html',subject_template_name='users/password_reset_subject.txt'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),name='password_reset_complete'),
      
] 