import json

from rest_framework import exceptions, authentication

from utilityservice.service.autoauthenticate import AutoAuth


class AutoAuthenticate(authentication.BaseAuthentication):
    def authenticate(self,request):
        auth_service = AutoAuth()
        auth_service.authenticate(request)
        if request.user is None:
            raise exceptions.AuthenticationFailed('Invalid credentials/token.')
        else:
            return request.user, None