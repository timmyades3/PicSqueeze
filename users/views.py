from django.template import RequestContext
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Verification_status
from .forms import Createuserform, Updateuserform, ProfileUpdateForm
import random
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone


class Register(View, LoginRequiredMixin):
    def post(self, request):

        if request.user.is_authenticated:
            return redirect('compress')
        else:
            form = Createuserform(request.POST)
            if form.is_valid():
                tac = request.POST.get('termsandcondition')
                if tac:
                    form.save()
                    username = form.cleaned_data.get('username')
                    messages.success(
                        request, f'Welcome {username} you have succesfully created an account')
                    return redirect('login')
                else:
                    messages.info(
                        request, 'term and conditions must be accepted')

            return render(request, 'register.html', {'form': form})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('compress')
        else:
            form = Createuserform()
        return render(request, 'register.html', {'form': form})


class Custom_login(View):
    def post(self, request):
        if request.user.is_authenticated:
            return redirect('compress')
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')
            r_me = request.POST.get('r_me')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if r_me:
                    request.session.set_expiry(600)
                else:
                    request.session.set_expiry(0)

                login(request, user)
                return redirect('compress')
            else:
                error_message = 'Invalid username or password.'
                return render(request, 'login.html', {'error_message': error_message})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('compress')
        return render(request, 'login.html')


class Profile(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'login'

    def post(self, request):

        u_form = Updateuserform(request.POST)
        if u_form.is_valid():
            u_form.save()

    def get(self, request):
        u_form = Updateuserform()
        user_ip = self.get_ip_address(request)
        context = {'user_ip': user_ip}
        return render(request, 'profile.html', context)

    def get_ip_address(self, request):
        user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if user_ip_address:
            ip = user_ip_address.split(',')[0]
            print(ip)
        else:
            ip = request.META.get('REMOTE_ADDR')
            print(ip)
        return ip


class Verification(LoginRequiredMixin, View):
    OTP_EXPIRATION_TIME = 60

    def generate_otp(self):
        return random.randint(100000, 999999)
   
    def send_otp_email(self, otp, request):
        user_email = request.user.email
        template = render_to_string('verification_email.html', {
                                    'name': request.user.first_name})
        subject = 'Verification OTP'
        message = template
        from_email = settings.EMAIL_HOST_USER  # Replace with your email
        recipient = user_email
        send_mail(subject, message, from_email, recipient)

    def post(self, request):
        user_otp = request.POST.get('otp')
        user = request.user
        try:
            verification_status = Verification_status.objects.get(user=user)
        except Verification_status.DoesNotExist:
            verification_status = None

        if verification_status:
            db_otp = verification_status.verification_otp
            if user_otp == str(db_otp):
                verification_status.is_verified = True
                verification_status.save()
            else:
                verification_status.is_verified = False
                verification_status.save()
        else:
            generated_otp = self.generate_otp()

            Verification_status.objects.create(
                user=user, verification_otp=generated_otp)

        return render(request, 'verification.html')

    def get(self, request):
        user = request.user
        
        
        
        try:
            verification_status = Verification_status.objects.get(user=user)
        except Verification_status.DoesNotExist:
            verification_status = None
        if not verification_status:
            generated_otp = self.generate_otp()
            Verification_status.objects.create(
                user=user, verification_otp=generated_otp)
            
        return render(request, 'verification.html')


class Logoutuser(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'login'

    def get(self, request):
        logout(request)
        return render(request, 'logout.html')
