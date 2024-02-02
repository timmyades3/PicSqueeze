from django.template import RequestContext
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import OtpToken
from .forms import Createuserform, Updateuserform
import random
from django.utils import timezone
from .utils import Util
from django.template.loader import render_to_string



class Register(View, LoginRequiredMixin):
    def post(self, request):
        if request.user.is_authenticated:
            return redirect("compress")
        else:
            form = Createuserform(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get("username")
                return redirect("verify-email", username=username)

            return render(request, "register.html", {"form": form})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("compress")
        else:
            form = Createuserform()
        return render(request, "register.html", {"form": form})


class Custom_login(View):
    def post(self, request):
        if request.user.is_authenticated:
            return redirect("compress")
        else:
            username = request.POST.get("username")
            password = request.POST.get("password")
            r_me = request.POST.get("r_me")

            user = authenticate(request, username=username, password=password)
            
            # if '@' in username:
            #     user_exist = User.objects.get(email=username)
            # else:    
            # user_exist = User.objects.filter(username=username).exists() 
            # print(user_exist)
            if user is not None and user.is_active == False: 
                return redirect("verify-email", username=username)
            if user is not None:
                if r_me:
                    request.session.set_expiry(600)
                else:
                    request.session.set_expiry(0)

                login(request, user)
                messages.success(
                    request,
                    f"Welcome {username} you have succesfully created an account",
                )
                if 'next' in request.POST: 
                    return redirect(request.POST['next'])
                return redirect("compress")   
            # elif user_exist == True and user is None :
            #     error_message = "Invalid password"
            else:
                error_message = "User does not exist."
                return render(request, "login.html", {"error_message": error_message})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("compress")
        return render(request, "login.html")


class Verify_email(View):
    def post(self,request, username):
        user = User.objects.get(username=username)
        user_otp = OtpToken.objects.filter(user=user).last()
        
        # valid token
        if user_otp.otp_code == request.POST['otp_code']:
            
            # checking for expired token
            if user_otp.otp_expires_at > timezone.now():
                user.is_active=True
                user.save()
                messages.success(request, "Account activated successfully!! You can Login.")
                return redirect("login")
            
            # expired token
            else:
                messages.warning(request, "The OTP has expired, get a new OTP!")
                return redirect("verify-email", username=user.username)
        
        # invalid otp code
        else:
            messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
            return redirect("verify-email", username=user.username)

    def get(self,request,username):
        user = User.objects.get(username = username)
        if request.user.is_authenticated:
            return redirect('compress')
        elif user.is_active == True:
            return redirect('login')
        # if user.is_superuser:
        #     pass
        
        # else:
        #     OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
        #     user.is_active=False 
        #     user.save()
        
        
        # # email credentials
        # otp = OtpToken.objects.filter(user=user).last()
       
       
        # subject="Email Verification"
        # email_body = f"""
        #                         Hi {user.username}, here is your OTP {otp.otp_code} 
        #                         it expires in 5 minute, use the url below to redirect back to the website
        #                         http://127.0.0.1:8000/verify-email/{user.username}
                                
        #                         """
        # # sender = "clintonmatics@gmail.com"
        # receiver = user.email 
        # data = {'email_body':email_body, 'to_email':receiver, 'email_subject':subject}

        # # send email
        # Util.send_email(data)
      
        context = {}
        return render(request, "verify_token.html", context)


class ResendOtp(View):
    def post(self,request):
        if request.user.is_authenticated:
            return redirect('compress')
        user_email = request.POST["otp_email"]
        
        if User.objects.filter(email=user_email).exists():
            user = User.objects.get(email=user_email)
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            
            
            # email variables
            subject="Email Verification"
            context = {
                'user': user,
                'otp': otp.otp_code,
                'protocol': 'https', 
                'domain': '127.0.0.1:8000'
            }
            email_body = render_to_string("verification_email.html", context)

            receiver = user.email
        
            data = {'email_body':email_body, 'to_email':receiver, 'email_subject':subject}

            # send email
            Util.send_email(data)

            
            messages.success(request, "A new OTP has been sent to your email-address")
            return redirect("verify-email", username=user.username)

        else:
            messages.warning(request, "This email dosen't exist in the database")
            return redirect("resend-otp")
        

    def get(self,request):
        if request.user.is_authenticated:
            return redirect('compress')               
        return render(request, "resend_otp.html")


class Profile(LoginRequiredMixin, View):
    def post(self, request):
        u_form = Updateuserform(request.POST)
        if u_form.is_valid():
            u_form.save()

    def get(self, request):
        u_form = Updateuserform()
        user_ip = self.get_ip_address(request)
        context = {"user_ip": user_ip}
        return render(request, "profile.html", context)

    def get_ip_address(self, request):
        user_ip_address = request.META.get("HTTP_X_FORWARDED_FOR")
        if user_ip_address:
            ip = user_ip_address.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip



class Logoutuser(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = "login"

    def get(self, request):
        logout(request)
        return redirect("login")
