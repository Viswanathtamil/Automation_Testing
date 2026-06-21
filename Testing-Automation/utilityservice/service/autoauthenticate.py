
from knox.auth import TokenAuthentication
from userservice.models.usermodels import Employee
from Automation.settings import SERVER_IP
from django.http import request, HttpRequest


class AutoAuth:

    def get_token(self, request):
        token = None
        if 'Authorization' in request.headers:
            token = request.META['HTTP_AUTHORIZATION']
            token_arr = token.split()
            if len(token_arr) == 2 and token_arr[0] == 'Token':
                token = token_arr[1]
        else:
            token = request.GET.get('token', None)
        return token

    def get_employee_id(self, user_id):
        emp_obj = Employee.objects.get(user_id=user_id)
        return emp_obj.id

    def get_path(self, request):
        path= request.build_absolute_uri()

        app_path = path.replace(SERVER_IP,'')
        path_arr = app_path.split("/")
        context = path_arr[1]
        context_path = '/' + context
        return context_path

    def authenticate(self, request):
        if 'Authorization' in request.headers:
            token = request.META['HTTP_AUTHORIZATION']
            token_arr = token.split()
            if len(token_arr) == 2 and token_arr[0] == 'Token':
                token = token_arr[1]
        else:
            token = request.GET.get('token', None)
        if token is not None:
            token_auth_obj = TokenAuthentication()
            token_utf8 = token.encode("utf-8")
            try:
                token_obj = token_auth_obj.authenticate_credentials(token_utf8)
                if token_obj is not None:
                    user = token_obj[0]
                    request.user = user
            except Exception as e:
                request.user = None
        else:
            request.user = None
