from django.db import models


class Uploadimage(models.Model):
    image = models.ImageField(upload_to='uploads',
                              max_length=1028, null=True)

    def __str__(self):
        return f'{self.image.name}'
