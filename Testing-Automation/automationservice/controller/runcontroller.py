import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes
from automationservice.controller.schedularfile import automation_schedular
from automationservice.service.runservice import automationserv,Report,runserv,masterserv
from utilityservice.vysfinpage import VysfinPage
from userservice.authservice.authservice import VysfinAuthentication

@csrf_exempt
@api_view(['POST','GET'])
@authentication_classes([VysfinAuthentication])
# @permission_classes([IsAuthenticated, VysfinPermission])
def test_temp_create(request):
    user_id = request.user.id
    if request.method == 'POST':
        data=json.loads(request.body)
        value = request.GET.get('value')
        service=automationserv().template_create(data,int(value),user_id)
        return HttpResponse(service.get(), content_type='application/json')
    else:
        id = request.GET.get('id')
        service = automationserv().get_template(id)
        return HttpResponse(service.get(), content_type='application/json')

@csrf_exempt
@api_view(['GET'])
def test_case_report(request):
    id = request.GET.get('id')
    code = request.GET.get("code")
    clientnme = request.GET.get("clientname")
    envirnment = request.GET.get('env')
    module = request.GET.get('module')
    from_date = request.GET.get('fromdate')
    to_date = request.GET.get('todate')
    batchcode = request.GET.get("batch_code")
    report = Report()
    return report.test_report_pdf(clientnme,module,from_date,to_date,code,envirnment,id,batchcode)

@csrf_exempt
@api_view(['POST'])
@authentication_classes([VysfinAuthentication])
# @permission_classes([IsAuthenticated, VysfinPermission])
def automation_runprocess(request):
    user_id = request.user.id
    client = request.GET.get("clientname")
    testcasecode=request.GET.get("Testcasecode")
    testcase_id = request.GET.get("testcase_id")
    call_vendor = automation_schedular(testcasecode, client, testcase_id,user_id)
    response = HttpResponse(call_vendor, content_type='application/json')
    return response


@csrf_exempt
@api_view(['POST'])
def client_master(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        resp_obj = masterserv().insert_client(data)
        return HttpResponse(resp_obj, content_type='application/json')

@csrf_exempt
@api_view(['POST'])
def module_master(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        resp_obj = masterserv().insert_module(data)
        return HttpResponse(resp_obj.get(), content_type='application/json')

def run_processtemplate(request):
    return render(request, 'testcase.html')
def template_form(request):
    return render(request, 'createtesttemplate.html')

def run_processreport (request):
    return render(request, 'reportdownload.html')

def template_summary_form(request):
    # username = request.user.username
    return render(request, 'template_summary.html')
def report_summary_form(request):
    return render(request, 'report_summary.html')
def run_summary_form(request):
    return render(request, 'run_summary.html')
def view_report_form(request):
    return render(request, 'report_view.html')

@csrf_exempt
@api_view(['GET','DELETE'])
@authentication_classes([VysfinAuthentication])
# @permission_classes([IsAuthenticated, VysfinPermission])
def template_summary(request):
    if request.method == 'GET':
        page = request.GET.get('page', 1)
        status = request.GET.get('status')
        client = request.GET.get('client')
        envir = request.GET.get('environment')
        module = request.GET.get('module')
        code = request.GET.get('code')
        page = int(page)
        vys_page = VysfinPage(page, 10)
        template = runserv()
        response_summary = template.template_summary(vys_page,status,client,envir,module,code)
        return HttpResponse(response_summary.get(), content_type='application/json')
    elif request.method == 'DELETE':
        id = request.GET.get('id')
        status = request.GET.get('active')
        template = runserv()
        response_summary = template.status_change(id,int(status))
        return HttpResponse(response_summary.get(), content_type='application/json')

@csrf_exempt
@api_view(['GET'])
def run_summary(request):
    page = request.GET.get('page', 1)
    status = request.GET.get('status')
    client = request.GET.get('client')
    envir = request.GET.get('environment')
    module = request.GET.get('module')
    code = request.GET.get('code')
    page = int(page)
    vys_page = VysfinPage(page, 10)
    template = runserv()
    response_summary = template.run_summary(vys_page,status,client,envir,module,code)
    return HttpResponse(response_summary.get(), content_type='application/json')

@csrf_exempt
@api_view(['GET'])
@authentication_classes([VysfinAuthentication])
def report_summary(request):
    user_id = request.user.id
    page = request.GET.get('page', 1)
    page = int(page)
    vys_page = VysfinPage(page, 10)
    client = request.GET.get('client')
    envir = request.GET.get('environment')
    module = request.GET.get('module')
    code = request.GET.get('code')
    status = request.GET.get('status')
    from_date = request.GET.get('fromDate')
    to_date = request.GET.get('toDate')
    batch_code = request.GET.get('batch_code')
    report = runserv()
    response_summary = report.report_summary(vys_page,client,envir,module,code,status,from_date,to_date,batch_code,user_id)
    return HttpResponse(response_summary.get(), content_type='application/json')

@csrf_exempt
@api_view(['GET'])
def view_report(request):
    id = request.GET.get('id')
    batchcode = request.GET.get('batch_code')
    report = Report()
    response = report.view_report(id, batchcode)
    # return render(request, 'report_view.html', context)
    # return HttpResponse(response.get(), content_type='application/json')
    return JsonResponse({'records': response})
    # return render(request, 'report_template.html', {'records': response})


@csrf_exempt
@api_view(['POST'])
def run_process_summary(request,test_id):
    serv=runserv().process_summary(test_id)
    return JsonResponse(serv, safe=False)

@csrf_exempt
@api_view(['GET'])
@authentication_classes([VysfinAuthentication])
def return_test_scn_name(request):
    user_id = request.user.id
    testcasecode= request.GET.get("Testcasecode")
    serv=runserv().get_scnario_name(testcasecode,user_id)
    response = JsonResponse(serv, safe=False)
    return response
@csrf_exempt
@api_view(['GET'])
@authentication_classes([VysfinAuthentication])
def test_case_summary(request):
    user_id = request.user.id
    batch_code= request.GET.get("batch_code")
    page = request.GET.get('page', 1)
    page = int(page)
    vys_page = VysfinPage(page, 10)
    serv = runserv().get_testcase(batch_code, user_id, vys_page)
    return HttpResponse(serv.get(), content_type='application/json')

@csrf_exempt
@api_view(['POST'])
def dropdown_testcase(request):
    clientname= request.GET.get("clientname")
    module=request.GET.get("module")
    environment=request.GET.get("environment")
    serv=runserv().dropdown_teastcasecode(clientname,module,environment)
    response = JsonResponse(serv, safe=False)
    return response

@csrf_exempt
@api_view(['GET'])
@authentication_classes([VysfinAuthentication])
def batch_summary(request):
    user_id = request.user.id
    page = request.GET.get('page', 1)
    status = request.GET.get('status')
    client = request.GET.get('client')
    envir = request.GET.get('environment')
    module = request.GET.get('module')
    code = request.GET.get('code')
    from_date = request.GET.get('fromDate')
    to_date = request.GET.get('toDate')
    page = int(page)
    vys_page = VysfinPage(page, 10)
    template = runserv()
    response_summary = template.batch_summary(vys_page,status,client,envir,module,code,from_date,to_date,user_id)
    return HttpResponse(response_summary.get(), content_type='application/json')