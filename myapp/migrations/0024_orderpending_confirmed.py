# Generated by Django 3.0 on 2021-03-11 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0023_auto_20210309_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderpending',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
