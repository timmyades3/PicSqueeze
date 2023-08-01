from django.contrib import admin
from .models import Profile,Logged_in_user,Verification_status

# Register your models here.

admin.site.register(Profile)
admin.site.register(Logged_in_user)
admin.site.register(Verification_status)

