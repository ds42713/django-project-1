# Generated by Django 3.0 on 2021-01-28 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_remove_allproduct_imageurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='allproduct',
            name='imageurl',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
