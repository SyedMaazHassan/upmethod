# Generated by Django 3.0.8 on 2021-12-20 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_systemuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SystemUser',
        ),
    ]