from django.urls import path
from . import views
from api.views import *
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

urlpatterns = [
    # path('', views.index, name="index"),
    # path('scripts', GetScriptApi.as_view()),
    # path('scripts/<id>', GetScriptApi.as_view()),
    path('user/<uid>', UserApi.as_view()),
    path('user/<uid>/<platform>/add', UserApi.as_view()),

    # path('user/<uid>/add', UserApi.as_view()),
    # path('user/<uid>/update', UserApi.as_view())

    # path('auth/checktoken', AuthenticationApi.as_view()),
    # path('auth/<action>', AuthenticationApi.as_view()),

    # path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('scripts/', GetParticularScriptApi.as_view()),
    # path('get-employees/', GetEmployeeApi.as_view()),
    # path('save-employee/', SaveEmployeeApi.as_view()),
    # path('update-employee/', UpdateEmployeeApi.as_view()),
    # path('delete-employee/', DeleteEmployeeApi.as_view()),
    # path('undelete-employee/', UndeleteEmployeeApi.as_view()),
    # path('get-company-info/', GetCompanyApi.as_view()),
    # path('update-company-info/', UpdateCompanyApi.as_view()),
    
]

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
