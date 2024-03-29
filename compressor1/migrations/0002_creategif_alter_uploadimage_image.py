# Generated by Django 4.2.1 on 2023-05-29 09:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compressor1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Creategif',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', 'mkv'])])),
                ('gif_image', models.ImageField(max_length=1028, null=True, upload_to='gif-images')),
            ],
        ),
        migrations.AlterField(
            model_name='uploadimage',
            name='image',
            field=models.ImageField(max_length=1028, null=True, upload_to='uncompressed'),
        ),
    ]
