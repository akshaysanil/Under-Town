# Generated by Django 4.0.5 on 2022-06-30 05:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_cartitem_variation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='variation',
            new_name='variations',
        ),
    ]
