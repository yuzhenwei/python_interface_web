# -*- coding:utf-8 -*

from django.http.response import HttpResponse
from DB.models import *
from django.db.models import Q
import json


"""用例集维护接口
__author__ = 'zijing'
接口统一返回值字段
retcode:0:执行成功！-1数据获取失败 ！-2数据更新失败 ！-3用例名已存在！请换个名字 -4接口列表不存在此接口或存在多个接口
code:0成功！-1请求方式错误！-2请求参数错误！
"""


def method_must_be_post(func):
    def inner(request, *args):
        if request.method == 'POST':
            result = func(request, *args)
            return result
        else:
            return HttpResponse(json.dumps({"code": -1,
                                            "msg": "请求方式错误！"}))
    return inner


# 根据用例集id查询此用例集下的接口用例，values字段变了js里也要变
@method_must_be_post
def cases_get_from_suite(request):
    suite_id = request.POST.get("suite_id", None)
    offset = request.POST.get('offset')
    limit = request.POST.get('limit')
    query_interface_name = request.POST.get('query_interface_name')
    query_case_name = request.POST.get('query_case_name')
    if suite_id:
        try:
            # Template_info表
            # Template_detail表usercaseid,
            # User_case表id,rejoin_key,paraminfo,interfaceurl,usercasename
            # Interface_info表id,pname,mname,interfacename,type
            td = list(Template_detail.objects.filter(
                Q(usercaseid__usercasename__contains=query_case_name) & Q(interfaceid__interfacename__contains=query_interface_name)
            ).filter(templateid_id=suite_id, isdelete=0, usercaseid__isdelete=0).values("usercaseid__id",
             "interfaceid__interfacename", "usercaseid__interfaceurl", "usercaseid__usercasename").order_by("-usercaseid__id"))
            # 获取所有的用例集名称"msg": td, "casemsg":casetb
            # casetb = list(User_case.objects.filter(isdelete=0).values("id", "usercasename"))
            case_lists = td[int(offset): int(limit) + int(offset)]
            return HttpResponse(json.dumps({"retcode": 0,
                                            "total": len(td),
                                            "rows": case_lists}))
        except:
            return HttpResponse(json.dumps({"retcode": -1,
                                            "total": 0,
                                            "rows": "",
                                            "msg":"数据获取失败 ！"}))
    else:
        return HttpResponse(json.dumps({"code": -2,
                                        "total": 0,
                                        "rows": "",
                                        "msg": "请求参数错误！"}))


# 关联信息tab 点击查询 调用接口
@method_must_be_post
def casesGetFromSuiteSupportCaseNameSearch(request):
    # 查询编辑关联用例集
    template_id = request.POST.get("t_id", None)
    casename = request.POST.get("casename", "")
    try:
        if casename != "":
            td = list(Template_detail.objects.filter(usercaseid__usercasename=casename,
                                                     templateid_id=template_id,
                                                     isdelete=0,
                                                     usercaseid_id__gt=0).exclude(usercaseid__usercasename="").values("interfaceid__id",
                                                                                                                      "id",
                                                                                                                      "interfaceid__interfacename",
                                                                                                                      "usercaseid__usercasename",
                                                                                                                      "usercaseid").order_by("-id"))
        else:
            td = list(
                Template_detail.objects.filter(templateid_id=template_id,
                                               isdelete=0,
                                               usercaseid_id__gt=0).exclude(usercaseid__usercasename="").values("interfaceid__id",
                                                                                                                "id",
                                                                                                                "interfaceid__interfacename",
                                                                                                                "usercaseid__usercasename",
                                                                                                                "usercaseid").order_by("-id"))
        return HttpResponse(json.dumps({"retcode": 0,
                                        "msg2": td}))
    except:
        return HttpResponse(json.dumps({"retcode": -2,
                                        "msg": "数据更新失败 ！"}))


#单个添加用例到用例集或者修改后保存--暂时没有用，后续修改
@method_must_be_post
def case_add_to_suite(request):
    case_name = request.POST.get("case_name", None)
    param_info = request.POST.get("param_info", None)
    interfaceid = request.POST.get("interfaceid", None)
    isequal = request.POST.get("isequal","")
    isnotequal = request.POST.get("isnotequal", "")
    iscontain = request.POST.get("iscontain", "")
    isnotcontain = request.POST.get("isnotcontain", "")
    isheader = request.POST.get("isheader", 0)
    headerinfo = request.POST.get("headerinfo", "")
    isjoin = request.POST.get("isjoin", 0)
    joininfo = request.POST.get("join_info", "")

    caseobj = User_case(interfaceid_id=interfaceid, paraminfo=param_info,isequal=isequal, isnotequal=isnotequal,
                      iscontain=iscontain, isnotcontain=isnotcontain, usercasename=case_name, isjoin=isjoin,
                      isheader=isheader, headerinfo=headerinfo, joininfo=joininfo)
    caseobj.save()

    #修改用例集usercaseid
    templateid = request.POST.get("templateid", None)
    Template_detail.objects.filter(id=templateid).update(usercaseid_id=caseobj.id)
    return HttpResponse(json.dumps({"addmsg": 1}))


#删除 用例集中指定用例
@method_must_be_post
def case_del_from_suite(request):
    id=request.POST.get("id", None)
    if id:
        try:
            caseid = Template_detail.objects.filter(id=id).values('usercaseid')
            caseid = list(caseid)
            Template_detail.objects.filter(usercaseid__id=id).update(isdelete=1)
            if len(caseid) == 1:
                # print(id, caseid[0]['usercaseid'])
                User_case.objects.filter(id=caseid[0]['usercaseid']).update(isdelete=1)
            return HttpResponse(json.dumps({"retcode": 0,
                                            "msg": "删除成功！"}))
        except:
            return HttpResponse(json.dumps({"retcode": -2,
                                            "msg": "数据更新失败 ！"}))
    else:
        return HttpResponse(json.dumps({"code": -2,
                                        "msg": "请求参数错误！"}))


# 保存到用例集明细表，同时保存进用例表一个id，关联上。后续只修改数据即可
@method_must_be_post
def case_add_to_template_detail(request):
    interfaceid = request.POST.get("interfaceid", None)
    templateid = request.POST.get("templateid", None)
    interfaceurl= request.POST.get("interfaceurl", None)
    case_data=request.POST.get("case_data", None)
    try:
        # 添加用例集明细和用例表数据
        # case_default_data=Interface_info.objects.filter(id=interfaceid,isdelete=0).values("defaultpar")
        # case_default_data=list(case_default_data)
        # if(len(case_default_data)==1):
        obj2 = User_case.objects.create(interfaceid_id=interfaceid, interfaceurl=interfaceurl, paraminfo=case_data)
        obj = Template_detail(interfaceid_id=interfaceid, templateid_id=templateid, usercaseid_id=obj2.id)
        obj.save()
        return HttpResponse(json.dumps({"retcode": 0,
                                        "msg": "添加成功！",
                                        "addmsg": 1}))
        # else:
        #     return HttpResponse(json.dumps({"retcode": -4, "msg": "接口列表不存在此接口或存在多个接口"}))
    except:
        return HttpResponse(json.dumps({"retcode": -2,
                                        "msg": "数据更新失败 ！"}))


#更新用例数据，修改用例接口 旧版本btype=="12"
@method_must_be_post
def case_update_to_usercase(request):
    try:
        case_name = request.POST.get("case_name", None)
        case_url = request.POST.get("case_url", None)
        param_info = request.POST.get("param_info", None)
        isequal = request.POST.get("isequal", "")
        isnotequal = request.POST.get("isnotequal", "")
        iscontain = request.POST.get("iscontain", "")
        isnotcontain = request.POST.get("isnotcontain", "")
        isheader = request.POST.get("isheader", 0)
        headerinfo = request.POST.get("headerinfo", "")
        isNeeded = request.POST.get("isNeeded", "")
        rejoin_keys = request.POST.get("rejoin_keys", "")
        isjoin = request.POST.get("isjoin", 0)
        joininfo = request.POST.get("join_info", "")
        upcase_id = request.POST.get("upcase_id", None)
        run_order_id = request.POST.get("run_order", -1)
        if upcase_id:
            # 判断用例名称不能重复
            duplicate=User_case.objects.filter(usercasename=case_name, isdelete=0).exclude(id=upcase_id)
            duplicate=list(duplicate)
            if(len(duplicate)==0):

                User_case.objects.filter(id=upcase_id).update(paraminfo=param_info, isequal=isequal, isnotequal=isnotequal,
                                                              iscontain=iscontain, isnotcontain=isnotcontain,
                                                              usercasename=case_name, rejoin_key=rejoin_keys, isjoin=isjoin,
                                                              isheader=isheader, headerinfo=headerinfo, joininfo=joininfo,run_order=run_order_id,interfaceurl=case_url)
                return HttpResponse(json.dumps({"retcode": 0,
                                                "msg": "数据保存成功 ！"}))
            else:
                return HttpResponse(json.dumps({"retcode": -3,
                                                "msg": "用例名已存在！请换个名字"}))
        else:
            return HttpResponse(json.dumps({"retcode": -2,
                                            "msg": "用例id不存在 ！"}))
    except:
        return HttpResponse(json.dumps({"retcode": -2,
                                        "msg": "数据更新失败 ！"}))

"""
描述：批量删除用例数据,前端传入case_ids的list
作者:代代花
"""


def del_all_case(request):
    case_ids = list(request.POST.getlist("case_ids"))
    # print(case_ids)
    for ids in case_ids:
        try:
            case_case = User_case.objects.filter(id=ids, isdelete=0)
            case_details = Template_detail.objects.filter(usercaseid_id=ids, isdelete=0)
            if len(case_case) > 0:
                if len(case_details) > 0:
                    Template_detail.objects.filter(usercaseid_id=ids).delete()
                    User_case.objects.filter(id=ids).delete()
                else:
                    return HttpResponse(json.dumps({"code": -1,
                                                    "msg": "用例集明细表中已删除，但用例表中未删除",
                                                    "data": ids}))
            else:
                return HttpResponse(json.dumps({"code": -1,
                                                "msg": "此数据用例表中已删除",
                                                "data": ids}))
        except Exception:
            return HttpResponse(json.dumps({"code": -1,
                                            "msg": ids}))
    return HttpResponse(json.dumps({"code": 200,
                                    "msg": "删除成功！"}))


"""
描述：查询公共参数
作者:石龙子
"""
def getPublicPar(request):
    caselistid=request.POST.get("caselistid", 0)
    publicpar=list(Template_info.objects.filter(id=caselistid).values('publicpar'))
    return HttpResponse(json.dumps({"msg": publicpar[0]['publicpar']}))

"""
描述：修改公共参数
作者:石龙子
"""
def updatePublicPar(request):
    caselistid=request.POST.get("caselistid", 0)
    public_par=request.POST.get("public_par","")
    Template_info.objects.filter(id=caselistid).update(publicpar=public_par)
    return HttpResponse(json.dumps({"msg":"1"}))

