# Generated by Django 4.0.5 on 2022-07-27 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0011_rename_descprition_category_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='maincategory',
            name='count_sold',
            field=models.IntegerField(default=0),
        ),
    ]
