import json
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import logout
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated

from userservice.authservice.authservice import AuthService
from userservice.data.errorResponse import auth_error
from userservice.data.response import auth_resp, SuccessStatus, SuccessMessage
from userservice.models.usermodels import Employee, LogoutInfo
from userservice.data.authresponse import AuthResponse
from utilityservice.middleware.auth import AutoAuthenticate
from utilityservice.service.autopermission import AutoPermission
from django.shortcuts import render


@api_view(['POST'])
@csrf_exempt
def create_user(request):
    signup_json = json.loads(request.body)
    entity_id = signup_json["entity_id"]
    user_name = signup_json["user_name"]
    full_name = signup_json["full_name"]
    email_id = signup_json["email_id"]
    password = signup_json["password"]
    code = signup_json['code']
    user = User.objects.create_user(username= user_name, password=password)
    user.set_password(password)
    user.save()
    user_id = user.id
    Employee.objects.create(user_name=user_name, full_name=full_name, email_id=email_id, user_id=user_id,entity_id=entity_id,code=code)
    resp = auth_resp()
    resp.set_status(200)
    resp.set_message(user_name+' User Created Successfully')
    response = HttpResponse(resp.get(), content_type="application/json")
    return response



@api_view(['POST'])
@csrf_exempt
@authentication_classes([AutoAuthenticate])
@permission_classes([IsAuthenticated, AutoPermission])
def logout1(request):
    user_id = request.user.id
    try:
        del request.session['token']
        request.user.auth_token_set.all().delete()
    except:
        request.user.auth_token_set.all().delete()
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    employee = Employee.objects.get(user_id=user_id)
    LogoutInfo.objects.create(employee=employee.id, ip_address=ip, logout_date=timezone.now())
    logout(request)
    success_obj = auth_resp()
    success_obj.set_status(SuccessStatus.SUCCESS)
    success_obj.set_message(SuccessMessage.SUCCESSFULLY_LOGOUT)
    return HttpResponse(success_obj.get(), content_type='application/json')


def authtokenform(request):
    return render(request, 'login.html')


@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def auth_token(request):
    auth_json = json.loads(request.body)
    # entity_id = auth_json["entity_id"]
    user_name = auth_json["user_name"]
    password = auth_json["password"]
    service = AuthService()
    obj_resp = service.automation_authenticate(user_name, password)
    # logger.info('Auth Token generated')
    if obj_resp == 403 :
        error_response = auth_error()
        error_response.set_http_status(status.HTTP_403_FORBIDDEN)
        error_response.set_description('Invalid user account')
        print(error_response)
        response = HttpResponse(error_response, content_type="application/json")
        response.status_code = 403
    else:
        response = HttpResponse(obj_resp.get(), content_type="application/json")
    return response