from django.urls import path

from userservice.authcontroller import authcontroller

urlpatterns=[
    path('create_user', authcontroller.create_user, name='user'),
    path('auth_token', authcontroller.auth_token, name='user'),
    path("authtoken-form/",authcontroller.authtokenform,name='authtoken'),
    path('logout', authcontroller.logout1, name='user'),
    ]