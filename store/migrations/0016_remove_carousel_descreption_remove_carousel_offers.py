# Generated by Django 4.0.5 on 2022-07-14 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_remove_carousel_sub_category_carousel_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carousel',
            name='descreption',
        ),
        migrations.RemoveField(
            model_name='carousel',
            name='offers',
        ),
    ]
