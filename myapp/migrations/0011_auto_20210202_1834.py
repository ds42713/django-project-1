# Generated by Django 3.0 on 2021-02-02 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_auto_20210202_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allproduct',
            name='unit',
            field=models.CharField(default='-', max_length=200),
        ),
    ]
