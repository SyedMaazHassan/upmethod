from api.models import *
from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response
from rest_framework import exceptions
import copy
from django.urls import resolve
from api.models import *

class ApiResponse:
    def __init__(self):
        
        self.output_object = {
            'status': 404,
            'success': {
                'data': None,
                'message': None
            },
            'errors': None,
            'warnings': None
        }

    def get_related_courses(self, selected_category, user_obj):
        if selected_category:
            all_courses = Course.objects.filter(category = selected_category, available_on_free_trial = True)
            if user_obj.is_trial_taken and user_obj.is_fee_paid:
                all_courses = Course.objects.filter(category = selected_category)
        else:
            all_courses = Course.objects.filter(available_on_free_trial = True)
            if user_obj.is_trial_taken and user_obj.is_fee_paid:
                all_courses = Course.objects.all()
        return all_courses

    def add_payment_info(self, user):
        self.output_object['is_trial_taken'] = user.is_trial_taken
        self.output_object['is_trial_end'] = user.is_trial_end
        last_payment = Payment.objects.filter(user = user, status = 1).last()
        pay_status = False
        if last_payment:
            if last_payment.is_expired():
                user.is_fee_paid = False
            else:
                user.is_fee_paid = True
                pay_status = True
            user.save()
        self.output_object['is_fee_paid'] = pay_status


    def unlock_first_level_mission(self, user, course):
        all_levels = Level.objects.filter(course = course)
        print("Checking if levels exists in this course")
        if all_levels.count() > 0:
            print("yes exists")
            first_level = all_levels[0]
            # Adding in UnlockLevel model
            print("Unlocking first level")
            unlocked_level_object = UnlockedLevel.objects 
            if not unlocked_level_object.filter(level = first_level, user = user).exists():
                unlocked_level_object.create(
                    level = first_level,
                    user = user
                )

                all_missions = Mission.objects.filter(level = first_level)
                print("Checking if mission exists in this level")
                if all_missions.count() > 0:
                    print("yes exists")
                    first_mission = all_missions[0]

                    # Adding in UnlockMission
                    print("Unlocking first mission")
                    unlocked_mission_object = UnlockedMission.objects 
                    if not unlocked_mission_object.filter(mission = first_mission, user = user).exists():
                        unlocked_mission_object.create(
                            mission = first_mission,
                            user = user
                        )
                    print("First mission unlocked")
                return

            print("Not mission exist")
        print("Not Level exist")

    def postSuccess(self, data, message):
        self.output_object['status'] = 200
        self.output_object['success']['data'] = data
        self.output_object['success']['message'] = message

    def postError(self, error_object):
        self.output_object['status'] = 404
        self.output_object['errors'] = error_object


class RequestAuthentication(BaseAuthentication, ApiResponse):
    def __init__(self):
        self.user_auth_list = ['CategoryApi', 'LevelApi', 'MissionApi', 'SubscriptionApi', 'PaymentApi']
        ApiResponse.__init__(self)

    def authenticateApiKey(self, request):
        status = False
        message = None
        if 'api_key' not in request.headers:
            message = "API key is missing"
            return (status, message)
        try:
            ApiToken.objects.get(key = request.headers['api_key'])
            status = True
        except ApiToken.DoesNotExist:
            message = "Given api key is not valid or it has expired"
        except Exception as e:
            message = str(e).replace("['", '').replace("']", '')
        return (status, {'api_key': message}) 


    def authenticateUid(self, request):
        status = False
        message = None
        if 'uid' not in request.headers:
            message = "User credentials not provided in headers"
            return (status, message)
        try:
            user = SystemUser.objects.get(uid = request.headers['uid'])
            status = True

            if not user.is_trial_synced:
                all_trials = Trial.objects.filter(user = user, is_active=True)
                for trial in all_trials:
                    trial.update_status()
                user.is_trial_synced = True
                user.save()

        except SystemUser.DoesNotExist:
            message = "User with given UID does not exist"
        except Exception as e:
            message = str(e).replace("['", '').replace("']", '')
        return (status, {'uid': message}) 


    def authenticate(self, request):
        api_check = self.authenticateApiKey(request)
        if not api_check[0]:
            self.postError(api_check[1])
            raise exceptions.AuthenticationFailed(self.output_object)

        requested_view = str(resolve(request.path_info).func.__name__)
        if requested_view in self.user_auth_list:
            user_check = self.authenticateUid(request)
            if not user_check[0]:
                self.postError(user_check[1])
                raise exceptions.AuthenticationFailed(self.output_object)

        return (True, None)