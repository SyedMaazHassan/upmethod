# Generated by Django 3.0.8 on 2022-02-25 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_systemuser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='systemuser',
            old_name='emai',
            new_name='email',
        ),
    ]
