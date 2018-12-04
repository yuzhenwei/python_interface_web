from django.conf.urls import url
from StatisticsManage import views

urlpatterns = [
    url(r'^statistics/',views.statistics),
]