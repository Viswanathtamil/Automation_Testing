from django.urls import path
from automationservice.controller import runcontroller


urlpatterns = [

    path('trstreport',runcontroller.test_case_report,name='report'),
    path('test_temp_create',runcontroller.test_temp_create,name='template'),
    path('automation_runprocess', runcontroller.automation_runprocess, name='runprocess'),
    path('create_client', runcontroller.client_master, name ='create_client'),
    path('create_module', runcontroller.module_master, name ='module_master'),
    path('template-form/', runcontroller.template_form, name='template_form'),
    path('run_processtemplate-form/', runcontroller.run_processtemplate, name='template_form'),
    path('report/', runcontroller.run_processreport, name='report'),
    path('template_summary', runcontroller.template_summary, name='template_summary'),
    path('run_summary', runcontroller.run_summary, name='run_summary'),
    path('report_summary', runcontroller.report_summary, name='report_summary'),
    path('template_summary-form/', runcontroller.template_summary_form, name='template_summary'),
    path('report_summary-form/', runcontroller.report_summary_form, name='report_summary'),
    path('run_summary-form/', runcontroller.run_summary_form, name='run_summary'),
    path('view_report-form/', runcontroller.view_report_form, name='report_view'),
    path('view_report', runcontroller.view_report, name='report_view'),
    path('run_process_summary/<test_id>',runcontroller.run_process_summary, name='run_process_summary'),
    path('test_case_summary',runcontroller.test_case_summary, name='test_case_summary'),
    path('return_test_scn_name', runcontroller.return_test_scn_name, name='return_test_scn_name'),
    path('dropdown_testcase', runcontroller.dropdown_testcase, name='dropdown_testcase'),
    path('batch_summary', runcontroller.batch_summary, name='batch_summary'),

]
