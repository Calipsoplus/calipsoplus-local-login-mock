from django.urls import path

from login.views import *

urlpatterns = [
    path('login/', login_user),
    path('login/umbrella/', check_umbrella_linked_account)
]