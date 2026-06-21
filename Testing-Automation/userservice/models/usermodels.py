from django.db import models
from django.utils.timezone import now

class Employee(models.Model):
    user_name = models.CharField(max_length=25)
    user_id = models.CharField(max_length=100,null=True)
    full_name = models.CharField(max_length=100)
    email_id = models.EmailField(null=True)
    first_name = models.CharField(max_length=100,null=True,blank=True)
    middle_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    designation = models.CharField(max_length=100,null=True,blank=True)
    grade = models.CharField(max_length=100,null=True,blank=True)
    gender = models.SmallIntegerField(default=1)
    entity_id = models.CharField(max_length=100,null=True)
    code = models.CharField(max_length=100,null=True)
    # phone_no = models.CharField(null=True , blank= True)

class Entity(models.Model):
    name = models.CharField(max_length=256)
    namespace = models.CharField(max_length=64)
    status = models.SmallIntegerField(default=1)

class LogoutInfo(models.Model):
    employee = models.IntegerField()
    ip_address = models.CharField(max_length=254)
    login_date = models.DateTimeField(default=now)
    logout_date = models.DateTimeField(default=now)