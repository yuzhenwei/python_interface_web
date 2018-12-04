from django.shortcuts import render, HttpResponse,redirect
import json
from DB.models import *


"""
接口列表页面，返回接口列表页面、项目的名称和接口的详细数据
"""


def interface_list(request):
    # 获取项目的数据
    pro_content =  list(Project_info.objects.all().values("pname", "pnumber"))
    if request.session.get('is_login', None):
        return render(request, "InterfacePage/interface_list.html", locals())
    else:
        return redirect("/web/login")



"""
单个删除接口数据，返回code值
"""
def interface_del(request):

    Interface_info.objects.filter(id=request.GET.get("id")).update(isdelete=1)

    return HttpResponse(json.dumps({"code": 200}))


"""
描述：批量删除接口数据,inter_ids
作者:代代花
"""


def del_all_interface(request):
    inter_ids = list(request.POST.getlist("inter_ids"))
    for ids in inter_ids:
        try:
            # 模板明细表里是否有关联接口的用例
            cases_t = Template_detail.objects.filter(interfaceid=ids, isdelete=0)
            # 用例表是否有关联接口的用例
            case_u = User_case.objects.filter(interfaceid=ids, isdelete=0)
            if len(cases_t) == 0:
                if len(case_u) == 0:
                    Interface_info.objects.filter(id=ids).delete()
                else:
                    return HttpResponse(json.dumps({"code": -2,
                                                    "msg": "用例表中仍有关联用例，不能删除此接口",
                                                    "data": ids}))
            else:
                return HttpResponse(json.dumps({"code": -3,
                                                "msg": "模板明细表中仍有关联用例，不能删除此接口",
                                                "data": ids}))
        except Exception:
            return HttpResponse(json.dumps({"code": -1,
                                            "msg": "删除失败！",
                                            "data": ids}))
    return HttpResponse(json.dumps({"code": 200,
                                    "msg": "删除成功！"}))


"""
根据项目的pnumber，查询模块的modelname、mnumber
"""


def search_pro(request):
    pnumber = request.GET.get("pnumber")
    pro_content = list(Project_model.objects.filter(pnumber=pnumber, isdelete=0).values("modelname","mnumber"))

    return HttpResponse(json.dumps({"code": 0,
                                    "msg": pro_content}))


"""
新增、修改接口
"""


def updata_interface(request):
    ids = request.POST.get("id")  # 获取ID
    interfacename = request.POST.get("interfacename")  # 接口名称
    url_adress = request.POST.get("url_adress")  # URL
    defaultpar = request.POST.get("defaultpar")  # 默认入参
    remark = request.POST.get("remark")  # 备注
    type = request.POST.get("type")  # 请求类型
    mnumber = request.POST.get("mnumber")  # 模块标识号
    pnumber = request.POST.get("pnumber")  # 项目表标识号
    pname = request.POST.get("pname")  # 项目名称
    mname = request.POST.get("mname")  # 模块名称
    # ID为不为空修改数据，ID为空新增数据
    if(ids != ''):

        model_id = Project_model.objects.get(mnumber=mnumber, isdelete=0)
        project_id = Project_info.objects.get(pnumber=pnumber, isdelete=0)
        Interface_info.objects.filter(id=ids).update(interfacename=interfacename, url=url_adress, defaultpar=defaultpar,
                                                     remark=remark, type=type, mnumber=model_id, pnumber=project_id,
                                                     pname=pname, mname=mname)
    else:
        model_id = Project_model.objects.get(mnumber=mnumber, isdelete=0)
        project_id = Project_info.objects.get(pnumber=pnumber, isdelete=0)
        Interface_info.objects.create(interfacename=interfacename, url=url_adress, defaultpar=defaultpar, remark=remark,
                                      type=type, mnumber=model_id, pnumber=project_id, pname=pname, mname=mname
                                      )
    return HttpResponse(json.dumps({"resultCode": 200}))


"""
分页查询
"""


def page_sel(request):
    try:
        # 获取模板编号
        model_id = Project_model.objects.get(mnumber=request.GET.get("mnumber"))
        # 获取项目编号
        project_id = Project_info.objects.get(pnumber=request.GET.get("pnumber"))
        query_name = request.GET.get('query_name')
        offset = request.GET.get('offset')
        limit = request.GET.get('limit')
    except:
        return HttpResponse(json.dumps({"retcode": 0,
                                        "total": 0,
                                        "rows": "",
                                        "msg": "查询出错！"}))

    try:
        interface_lists = list(Interface_info.objects.filter(interfacename__icontains=query_name).filter(
            pnumber=project_id, mnumber=model_id, isdelete=0).values("id", "interfacename", "url"))
        interface_list = interface_lists[int(offset):int(limit)+int(offset)]
        return HttpResponse(json.dumps({"retcode": 0,
                                        "msg": "sucess",
                                        "total": len(interface_lists),
                                        "rows": interface_list}))
    except:
        return HttpResponse(json.dumps({"retcode": -1,
                                        "total": 0,
                                        "rows": "",
                                        "msg": "查询出错！"}))
