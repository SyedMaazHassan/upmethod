# Generated by Django 3.0.8 on 2021-12-20 13:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20211220_1344'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
        ),
    ]
