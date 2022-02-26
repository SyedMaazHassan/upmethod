# Generated by Django 3.0.8 on 2022-02-25 17:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_delete_systemuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemUser',
            fields=[
                ('uid', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('avatar_url', models.URLField(blank=True, null=True)),
                ('display_name', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('emai', models.EmailField(max_length=254)),
                ('auth_type', models.CharField(choices=[('google', 'google'), ('fb', 'facebook')], max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]