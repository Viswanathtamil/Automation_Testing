
from django.contrib.auth import authenticate
from knox.models import AuthToken
from rest_framework import status
from rest_framework import authentication, exceptions
from userservice.data.authresponse import AuthResponse
from userservice.data.errorResponse import auth_error
from userservice.models.usermodels import Entity, Employee
from knox.auth import TokenAuthentication
import rest_framework


class AuthService:
    def get_user(self, user_name, password):
        user = authenticate(username=user_name, password=password)
        return user
    def automation_authenticate(self, user_name, password):
        user = self.get_user(user_name, password)
        if user is None:
            # error_response = auth_error()
            # error_response.set_http_status(status.HTTP_403_FORBIDDEN)
            # error_response.set_description('Invalid user account')
            # print(error_response)
            return 403
        else:
            user.auth_token_set.all().delete()
            token_obj = AuthToken.objects.create(user)
            employee = Employee.objects.filter(user_name=user_name)
            print(token_obj)
            auth_user = token_obj[0].user
            expiry = token_obj[0].expiry
            expiry_str = str(expiry)
            auth_response = AuthResponse()
            auth_response.set_token(token_obj[1])
            auth_response.set_expiry(expiry_str)
            auth_response.set_name(employee[0].full_name)
            auth_response.set_code(employee[0].code)
            auth_response.set_employee_id(employee[0].id)
            auth_response.user_id = employee[0].user_id
            auth_response.entity_id = employee[0].entity_id
            return auth_response

class VysfinAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = None
        user = None
        try:
            token = request.META['HTTP_AUTHORIZATION']
            token_arr = token.split()
            if not token_arr[0] == 'Token':
                raise exceptions.AuthenticationFailed(('No credentials provided.'))
            token = token_arr[1]
            print(token)
        except KeyError:
            try:
                token = request.META['HTTP_AUTHORIZATION']
                token_arr = token.split()
                if not token_arr[0] == 'Token':
                    raise exceptions.AuthenticationFailed(('No credentials provided.'))
                token = token_arr[1]
                tok = TokenAuthentication()
                token.encode("utf-8")
                tstr = token.encode("utf-8")
                token_obj = tok.authenticate_credentials(tstr)
                user = token_obj[0]
            except rest_framework.authtoken.models.Token.DoesNotExist:
                raise exceptions.AuthenticationFailed(('Invalid token.'))
            except:
                user = None

        if token is not None:
            print(token)
            tok = TokenAuthentication()
            token.encode("utf-8")
            tstr = token.encode("utf-8")
            token_obj = tok.authenticate_credentials(tstr)
            user = token_obj[0]

        else:
            user = None

        if user is None:
            token = request.GET.get('token', None)
            if token is not  None :
                tok = TokenAuthentication()
                token.encode("utf-8")
                tstr = token.encode("utf-8")
                token_obj = tok.authenticate_credentials(tstr)
                user = token_obj[0]

        return (user, None)