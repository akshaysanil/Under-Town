# Generated by Django 4.0.4 on 2022-07-15 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_remove_carousel_descreption_remove_carousel_offers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carousel',
            old_name='image',
            new_name='banner_image',
        ),
    ]
