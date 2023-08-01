import os
from django import forms
from .models import Uploadimage, Creategif


class UploadimageForm(forms.ModelForm):
    imageformat = forms.CharField(required=False)
    quality = forms.IntegerField(min_value=0, max_value=100, required=False)
    imageheight = forms.IntegerField(required=False)
    imagewidth = forms.IntegerField(required=False)

    class Meta:
        model = Uploadimage
        fields = ['image']

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')

        if image:
            image_format = image.content_type
            allowed_format = ['image/jpg', 'image/jpeg',
                              'image/png', 'image/webp', 'image/gif']
            if image_format not in allowed_format:
                self.add_error(
                    'image', 'image format not supported.image must be jpg,png,jpeg,webp or gif.')

        return cleaned_data


class CreategifForm(forms.ModelForm):
    gif_width = forms.IntegerField(required=False)
    gif_height = forms.IntegerField(required=False)
    gif_duration = forms.IntegerField(required=False)
    gif_name = forms.CharField(required=False)
    gif_images = forms.ImageField(required=False)

    class Meta:
        model = Creategif
        fields = ['video', 'gif_image']

    def clean(self):
        cleaned_data = super().clean()
        gif_images = cleaned_data.get('gif_images')

        if gif_images:
            img = str(gif_images)
            img_format = os.path.splitext(img)[1]
            allowed_format = ['.jpg', '.jpeg',
                              '.png', '.webp']
            if img_format not in allowed_format:
                self.add_error(
                    'gif_image', 'image format not supported.image must be jpg,png,jpeg,webp or gif.')

        return cleaned_data
