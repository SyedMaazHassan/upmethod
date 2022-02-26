from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from api.models import *

'''
This file contains serializers that is providing
validation and bring data from database safely
under the consideration of checking each parameter
and validate them properly 
'''

# Serializer for all the APIs related Script Model (table)

class CategorySerializer(serializers.ModelSerializer): 
    class Meta:
        model = Category
        fields = ["name"]

class TagSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Tag
        fields = ["name"]

class AllScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = ["id", "title", "poster", "created_at"]

class ScriptSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many = False, read_only = True)
    tags = TagSerializer(many = True, read_only = True)
    class Meta:
        model = Script
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    def validate(self, data):
        errors = {}
        if 'uid' not in data:
            print(data)
            errors['uid'] = ["This field is required"]

        if len(errors.keys()) > 0:
            raise serializers.ValidationError(errors)

        return data

    class Meta:
        model = SystemUser
        fields = "__all__"

