from django.conf.urls import url
from Login import views

urlpatterns = [
    url(r'^as/', views.login),
]