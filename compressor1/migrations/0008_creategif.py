# Generated by Django 3.2.21 on 2024-01-17 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compressor1', '0007_delete_creategif'),
    ]

    operations = [
        migrations.CreateModel(
            name='Creategif',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(blank=True, null=True, upload_to='uncreated_videos')),
                ('gif_image', models.ImageField(blank=True, max_length=1028, null=True, upload_to='uncreated_images')),
            ],
        ),
    ]
