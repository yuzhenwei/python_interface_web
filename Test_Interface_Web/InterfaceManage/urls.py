from django.conf.urls import url
from InterfaceManage import views_controller, views_quicktest, views_excel, views_detail

urlpatterns = [
    url(r'^list/', views_controller.interface_list),
    url(r'^del/', views_controller.interface_del),
    url(r'^search/', views_controller.search_pro),
    url(r'^upadte/', views_controller.updata_interface),
    url(r'^quicktest/', views_quicktest.main),
    url(r'^run/', views_quicktest.run_interface),
    url(r'^upload/', views_excel.upload_inter),
    url(r'^upload_case/', views_excel.upload_case),
    url(r'^down_inter_xls/', views_excel.downloadTest),
    url(r'^down_case_xls/', views_excel.downloadTest),
    url(r'^detail/', views_detail.interfaceDetail),
    url(r'^page_sel/', views_controller.page_sel),
    url(r'^batch_del/', views_controller.del_all_interface),
    url(r'^export_interface/', views_excel.export_interface),
    url(r'export_case/',views_excel.export_case)
]