from django.conf.urls import url
from Login import views
from TestCaseManage import views_caseSuites, views_interface, case_task_views, views_suite_management, views_casedetail,views_casecheck

urlpatterns = [
    url(r'^as/', views.login),
    url(r'^projectLists/', views_caseSuites.project_lists, name='projectLists'),
    url(r'^testcase_maintain/', views_interface.testcase_maintain),
    url(r'^testcaserunner/', views_interface.testcaserunner),
    url(r'^testcase_info/', views_interface.testcase_info),
    url(r'^casesuitelist/', views_caseSuites.testcase_list),
    url(r'^add/', views_caseSuites.add),
    url(r'^delete/', views_caseSuites.delete),
    # url(r'^run/', case_task_views.start_run_case),
    url(r'^checkrun/', views_casecheck.start_run_checkcase),        #带检查点
    url(r'^getCasesFromSuite/', views_suite_management.cases_get_from_suite),
    url(r'^deleteCaseFromSuite/', views_suite_management.case_del_from_suite),
    url(r'^getPublicPar/', views_suite_management.getPublicPar),        #查询公共参数
    url(r'^updatePublicPar/', views_suite_management.updatePublicPar),        #修改公共参数
    url(r'^addCaseToSuite/', views_suite_management.case_add_to_template_detail),
    url(r'^updateCaseToUserCase/', views_suite_management.case_update_to_usercase),
    url(r'^getCasesFromSuiteNameSearch/', views_suite_management.casesGetFromSuiteSupportCaseNameSearch),
    url(r'^start_init/', case_task_views.start_ini_templet),
    url(r'^caseDetail/', views_casedetail.casedetail),
    url(r'^batchDelete/', views_suite_management.del_all_case)
]