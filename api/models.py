from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User, auth
import uuid

# Create your models here.

# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver

# class Tag(mode)


class Category(models.Model):
    name = models.CharField(max_length = 50, unique = True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length = 50, unique = True)

    def __str__(self):
        return self.name

class Script(models.Model):
    title = models.CharField(max_length = 50)
    poster = models.ImageField(upload_to = "posters", null = True, blank = True)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, null = True, blank = True)
    created_at = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f'{self.title} ({self.category.name})'


class SystemUser(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.CharField(default = None, unique = True, max_length = 255)
    profile_picture = models.ImageField(upload_to = "profile-pictures", null = True, blank = True)
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)

    def __str__(self):
        return f"{self.first_name} - {self.uid}"


class ApiToken(models.Model):
    key = models.UUIDField(unique = True, default=uuid.uuid4, editable = False)

    def __str__(self):
        return str(self.key)
    
