from django.contrib import admin
from api.models import *
# Register your models here.
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Script)
admin.site.register(SystemUser)
admin.site.register(ApiToken)
