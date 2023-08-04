# Generated by Django 4.2.1 on 2023-05-29 14:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compressor1', '0002_creategif_alter_uploadimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creategif',
            name='gif_image',
            field=models.ImageField(max_length=1028, null=True, upload_to='uncreated_images'),
        ),
        migrations.AlterField(
            model_name='creategif',
            name='video',
            field=models.FileField(null=True, upload_to='uncreated_videos', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'mkv'])]),
        ),
    ]