from django.conf.urls import url
from JobManage import views

urlpatterns = [
    url(r'^job/',views.job),
]