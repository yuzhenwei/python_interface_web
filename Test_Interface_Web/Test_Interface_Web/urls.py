"""Test_Interface_Web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^db/',include('DB.urls')),
    url(r'^web/', include('Login.urls')),
    url(r'^project/', include('ProjectManage.urls')),
    url(r'^report/', include('ReportManage.urls')),
    url(r'^testcase/', include('TestCaseManage.urls')),
    url(r'^interface/', include('InterfaceManage.urls')),
    url(r'^job/', include('JobManage.urls')),
    url(r'^statistics/', include('StatisticsManage.urls')),
]
