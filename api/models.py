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
    uid = models.CharField(primary_key=True, max_length = 255)
    avatar_url = models.URLField(null = True, blank = True)
    display_name = models.CharField(max_length = 255)
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255, null = True)
    email = models.EmailField(unique = True, null = True)
    auth_type = models.CharField(max_length = 255, choices = [('google', 'google'), ('fb', 'facebook')])
    created_at = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f"{self.first_name} - {self.uid}"

class ApiToken(models.Model):
    key = models.UUIDField(unique = True, default=uuid.uuid4, editable = False)

    def __str__(self):
        return str(self.key)
    
