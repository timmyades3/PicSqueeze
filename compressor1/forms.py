import os
from django import forms
from .models import Uploadimage


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


