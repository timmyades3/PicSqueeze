from django.contrib import admin
from .models import Profile,Logged_in_user,OtpToken

# Register your models here.

admin.site.register(Profile)
admin.site.register(Logged_in_user)
admin.site.register(OtpToken)

