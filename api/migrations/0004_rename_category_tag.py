# Generated by Django 3.2.8 on 2021-11-08 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_script_poster'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='Tag',
        ),
    ]
