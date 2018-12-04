from django.conf.urls import url
from Login import views
from ReportManage import views

urlpatterns = [
    url(r'^report/',views.report),

    url(r'^testreport',views.interfaceresult,name="reprothtml"),

]