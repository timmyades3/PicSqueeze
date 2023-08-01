from django.contrib import admin
from .models import Uploadimage,Compressedimage,Creategif

# Register your models here.
admin.site.register(Uploadimage)
admin.site.register(Compressedimage)
class CreategifAdmin(admin.ModelAdmin):
    list_display = ('video', 'gif_image')

admin.site.register(Creategif, CreategifAdmin)