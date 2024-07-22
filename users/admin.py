from django.contrib import admin
from .models import Profile, Friend_Request

admin.site.register([Profile, Friend_Request])