# Generated by Django 4.0.5 on 2022-06-24 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0002_alter_category_options_alter_maincategory_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('product_image', models.ImageField(upload_to='products')),
                ('is_available', models.BooleanField(default=True)),
                ('stock', models.IntegerField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('brand', models.CharField(blank=True, max_length=100)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='category.category')),
                ('main_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='category.maincategory')),
                ('sub_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='category.subcategory')),
            ],
        ),
    ]
