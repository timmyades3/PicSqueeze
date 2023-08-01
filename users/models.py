from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class Logged_in_user(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='logged_in_user', on_delete=models.CASCADE)
    session_key = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Verification_status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    is_verified = models.BooleanField(default = False)
    verification_otp = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f'{self.user.username} verification status'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    termsandcondition = models.BooleanField(default=False,null=True)
   
    def __str__(self):
        return f'{self.user.username} profile'
