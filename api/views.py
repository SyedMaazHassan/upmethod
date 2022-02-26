from django.shortcuts import render
from api.serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import get_object_or_404
# Create your views here.
from api.models import *
from django.conf import settings
from api.authentication import RequestAuthentication, ApiResponse
from api.support import beautify_errors
import json
import requests
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication

# from rest_framework_simplejwt.tokens import RefreshToken
# import jwt


def index(request):
    return render(request, "abcc.html")


class UserApi(APIView, ApiResponse):
    authentication_classes = [RequestAuthentication]
    def __init__(self):
        self.platforms = ['google', 'fb']
        ApiResponse.__init__(self)

    def create_google_user(self, response_object):
        google_user = response_object['user']
        user = {
            'avatar_url': google_user['photo'],
            'display_name': google_user['givenName'],
            'first_name': google_user['givenName'],
            'last_name': google_user['familyName'],
            'email': google_user['email']
        }
        return user
    
    def get_fb_user(self, user_id, access_token):
        api_url = f'https://graph.facebook.com/{user_id}?fields=id,name,email,picture.type(large)&access_token={access_token}'
        response = requests.get(
            api_url,
            timeout = 6
        )
        output = response.json()
        return output
        
    def create_facebook_user(self, response_object):
        user_id = response_object['userID']
        access_token = response_object['accessToken']
        fb_user = self.get_fb_user(user_id, access_token)
        profile_pic = fb_user['picture']['data']['url']
        name_collection = fb_user['name'].split(' ')
        first_name = name_collection[0]
        last_name = name_collection[1]
        email = fb_user['email'] if 'email' in fb_user else None
        if len(first_name) > 1:
            last_name = ' '.join(name_collection[1:])
        user = {
            'avatar_url': profile_pic,
            'display_name': first_name,
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }
        return user

    def generate_user_object(self, platform, response_object):
        if platform in self.platforms:
            try:
                user = None
                if platform == 'google':
                    user = self.create_google_user(response_object)
                if platform == 'fb':
                    user = self.create_facebook_user(response_object)
                return (True, user)
            except Exception as e:
                return (False, str(e))
        else:
            return (False, "Invalid third party platform")
 
    def post(self, request, uid=None, platform=None):
        try:
            data = request.data
            user = self.generate_user_object(platform, data)
            if user[0]:
                user = user[1]
                user['auth_type'] = platform
                user['uid'] = uid
                serializer = UserSerializer(data = user)
                if serializer.is_valid():
                    serializer.save()
                    self.postSuccess({'user': serializer.data}, "User added successfully")
                self.postError(beautify_errors(serializer.errors))
            else:
                self.postError({'user': user[1]})
        except Exception as e:
            self.postError({ 'uid': str(e) })
        return Response(self.output_object)

    def get(self, request, uid=None):
        try:
            if not uid:
                raise Exception("UID is missing")
            user = get_object_or_404(SystemUser, uid=uid)
            serializer = UserSerializer(user, many = False)
            self.postSuccess({'user': serializer.data}, "User fetched successfully")
        except Exception as e:
            self.postError({ 'uid': str(e) })
        return Response(self.output_object)

    def patch(self, request, uid=None):
        try:
            user_obj = get_object_or_404(SystemUser, uid=uid)

            if user_obj.email != request.data['email']:
                self.postError({'email': 'To avoid problems with future signin, Email cannot be updated'})
                return Response(self.output_object)

            serializer = UserSerializer(user_obj, data=request.data, partial = True)
            
            if serializer.is_valid():
                serializer.save()
                self.postSuccess({'user': serializer.data}, "User updated successfully")
            else:
                self.postError(beautify_errors(serializer.errors))                 
        except Exception as e:
            self.postError({ 'uid': str(e) })
        return Response(self.output_object)
