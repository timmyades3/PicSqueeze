from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth import user_logged_in,user_logged_out
from django.dispatch import receiver
from django.db import transaction
from django.db.models.signals import post_save,m2m_changed
from .models import OtpToken, Profile,Logged_in_user
from django.utils import timezone
from .utils import Util
from django.template.loader import render_to_string
from social_django.models import UserSocialAuth



@receiver(post_save, sender=User)
def create_token(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            pass
        else:
            if len(instance.password) < 88:
                pass
            else:
                OtpToken.objects.create(user=instance, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
                instance.is_active=False 
                instance.save()
            
            
                # email credentials
                otp = OtpToken.objects.filter(user=instance).last()
            
            
                subject="Email Verification"
                context = {
                        'user': instance,
                        'otp': otp.otp_code,
                        'protocol': 'https', 
                        'domain': '127.0.0.1:8000'
                    }
                email_body = render_to_string("verification_email.html", context)

                receiver = instance.email 
                data = {'email_body':email_body, 'to_email':receiver, 'email_subject':subject}

                # send email
                Util.send_email(data)
        

@receiver(post_save, sender=User)
def createprofile(sender, instance, created, **kwargs):
    if created: 
        Profile.objects.create(user=instance)

@receiver(user_logged_in)
def on_user_logged_in(sender,**kwargs):
    Logged_in_user.objects.get_or_create(user=kwargs.get('user'))

@receiver(user_logged_out)
def on_user_logged_out(sender,**kwargs):
    Logged_in_user.objects.filter(user=kwargs.get('user')).delete()    