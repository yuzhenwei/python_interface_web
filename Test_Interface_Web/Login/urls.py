from django.conf.urls import url
from Login import views

urlpatterns = [
    url(r'^login/', views.login),
    url(r'^loginout/', views.logout),
    url(r'^index/', views.login_on),
    url(r'^interface_base/', views.interface_base),
]