# Generated by Django 3.0 on 2021-02-05 10:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0013_auto_20210205_1039'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pro_file',
            new_name='Profile',
        ),
    ]
