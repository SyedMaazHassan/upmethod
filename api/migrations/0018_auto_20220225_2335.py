# Generated by Django 3.0.8 on 2022-02-25 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20220225_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemuser',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='systemuser',
            name='last_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
