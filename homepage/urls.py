
from django.conf import settings
from django.urls import path, include
# import views from application
from .views import *

urlpatterns = [
    path('', homepage),
    path('runCheck/', runCheck),
    path('saveDevice/', saveDevice),
]
