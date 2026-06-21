from django.db import models
from django.utils.timezone import now

class Testcase_Scenario_Template(models.Model):
    client_name=models.CharField(max_length=256, null=True)
    Project_module=models.CharField(max_length=256, null=True)
    Testcase_scenario_name=models.CharField(max_length=256, null=True)
    Testcase_scenario_template=models.TextField(null=True, blank=True)
    environment = models.CharField(max_length=256, null=True)
    url = models.CharField(max_length=256, null=True)
    created_date = models.DateTimeField(default=now,null=True, blank=True)
    created_by=models.CharField(max_length=256, null=True)
    updated_date = models.DateTimeField(default=now,null=True, blank=True)
    updated_by = models.CharField(max_length=256, null=True)
    Steps = models.SmallIntegerField(null=True, blank=True)
    active = models.SmallIntegerField(default=1)
    full_partial = models.SmallIntegerField(default=1)
    Testcase_code = models.CharField(max_length=256, null=True)

class Testcase_Run(models.Model):
    Testcase_code= models.CharField(max_length=256, null=True)
    Testcase_template_input=models.TextField(null=True, blank=True)
    module=models.CharField(max_length=256, null=True)
    created_date = models.DateTimeField(default=now)
    created_by = models.CharField(max_length=256, null=True)
    updated_date = models.DateTimeField(default=now)
    updated_by = models.CharField(max_length=256, null=True)
    environment=models.CharField(max_length=256, null=True)
    url = models.CharField(max_length=256, null=True)
    client_name = models.CharField(max_length=256, null=True)
    status = models.CharField(max_length=256, null=True)
    temp_run = models.SmallIntegerField(default=1, null=True, blank=True)
    testcase_scn = models.ForeignKey(Testcase_Scenario_Template, on_delete=models.CASCADE, null=True, blank=True)
    Test_scnarios = models.TextField(max_length=200, blank=True, null=True)
    active = models.SmallIntegerField(default=1)
    full_partial = models.SmallIntegerField(default=1)
    batch_code = models.CharField(max_length=256, null=True)
    Testcase_scenario_name = models.CharField(max_length=256, null=True)

class Testcase_Result(models.Model):
    client_name = models.CharField(max_length=256, null=True)
    Testcase_code = models.CharField(max_length=256, null=True)
    status = models.CharField(max_length=16, null=True, blank=True)
    screenshoot = models.TextField(max_length=200, blank=True, null=True)
    Testcase_Result = models.CharField(max_length=16, null=True, blank=True)
    created_date = models.DateField(default=now)
    created_by = models.CharField(max_length=256, null=True)
    inputdata = models.TextField(null=True, blank=True)
    outputdata = models.TextField(null=True, blank=True)
    Module = models.CharField(max_length=256, null=True)
    remarks = models.TextField(max_length=200, blank=True, null=True)
    Test_scnarios = models.TextField(max_length=200, blank=True, null=True)
    Message = models.CharField(max_length=256, null=True)
    code = models.TextField(max_length=200, blank=True, null=True)
    statuscode = models.SmallIntegerField(default=1)
    environment = models.CharField(max_length=256, null=True)
    test_implement_status = models.CharField(max_length=256, null=True)
    batch_code = models.CharField(max_length=256, null=True)
    updated_date = models.DateTimeField(default=now)
    updated_by = models.CharField(max_length=256, null=True)
    Testcase_scenario_name = models.CharField(max_length=256, null=True)
    url = models.CharField(max_length=256, null=True)


class Client(models.Model):
    client_name=models.CharField(max_length=256, null=True)
    created_date = models.DateTimeField(default=now,null=True, blank=True)
    created_by=models.CharField(max_length=256, null=True)
    updated_date = models.DateTimeField(default=now,null=True, blank=True)
    updated_by = models.CharField(max_length=256, null=True)

class Module_master(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    Project_module = models.CharField(max_length=256, null=True)
    created_date = models.DateTimeField(default=now, null=True, blank=True)
    created_by = models.CharField(max_length=256, null=True)
    updated_date = models.DateTimeField(default=now, null=True, blank=True)
    updated_by = models.CharField(max_length=256, null=True)


class Test_run_process_summary(models.Model):
    Testcase_code = models.CharField(max_length=256, null=True)
    test_implement_status = models.CharField(max_length=256, null=True)
    percentage = models.TextField(max_length=256, null=True)
    Process_status=models.SmallIntegerField(default=0)
    Scenario_names= models.TextField(max_length=256, null=True)

class ScreenshotBlob(models.Model):
    file_path = models.CharField(max_length=500, unique=True)
    image_blob = models.BinaryField()

class Batchcode(models.Model):
    client_name = models.CharField(max_length=256, null=True)
    created_date = models.DateField(default=now)
    created_by = models.CharField(max_length=256, null=True)
    Module = models.CharField(max_length=256, null=True)
    environment = models.CharField(max_length=256, null=True)
    batch_code = models.CharField(max_length=256, null=True)
    updated_date = models.DateTimeField(default=now)
    updated_by = models.CharField(max_length=256, null=True)
    status = models.CharField(max_length=256, null=True)