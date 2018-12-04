from django.conf.urls import url
from Login import views
from ProjectManage import views

urlpatterns = [
    url(r'^search/', views.search),
    url(r'^add_project/', views.add_project),
    url(r'^edit_project/', views.edit_project),
    url(r'^delete_project/', views.delete_project),
    url(r'^projectLists/', views.project_lists),
]