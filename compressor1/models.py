from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.


class Uploadimage(models.Model):
    image = models.ImageField(upload_to='uncompressed',
                              max_length=1028, null=True)

    def __str__(self):
        return f'{self.image.name}'


class Compressedimage(models.Model):
    compressed_image = models.ImageField(upload_to='compressed', null=True)

    def __str__(self):
        return f'{self.compressed_image.name}'


class Creategif(models.Model):
    video = models.FileField(
        upload_to='uncreated_videos', null=True, blank=True)
    gif_image = models.ImageField(
        upload_to='uncreated_images', max_length=1028, null=True, blank=True)
