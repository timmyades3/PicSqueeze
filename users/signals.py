from django.contrib.auth.models import User
from django.contrib.auth import user_logged_in,user_logged_out
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile,Logged_in_user
from .forms import ProfileUpdateForm


@receiver(post_save, sender=User)
def createprofile(sender, instance, created, **kwargs):
    if created: 
        Profile.objects.create(user=instance,termsandcondition=True)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(user_logged_in)
def on_user_logged_in(sender,**kwargs):
    Logged_in_user.objects.get_or_create(user=kwargs.get('user'))

@receiver(user_logged_out)
def on_user_logged_out(sender,**kwargs):
    Logged_in_user.objects.filter(user=kwargs.get('user')).delete()    