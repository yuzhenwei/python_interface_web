# -*- coding:utf-8 -*
from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from DB.models import *
import json


# bootstrap-table分页
def project_lists(request):
    offset = request.GET.get('offset')
    limit = request.GET.get('limit')
    pname = request.GET.get('pname')
    try:
        if(pname == '' or pname == None or pname == '--请选择--'):
            projectLists = list(Template_info.objects.filter(isdelete=0).order_by('-id').values("id","pnumber__pname","templatename"))
        else:
            projectLists = list(Template_info.objects.filter(isdelete=0,pnumber__pname=pname).order_by('-id').values("id","pnumber__pname","templatename"))
        data = projectLists[int(offset):int(limit)+int(offset)]
        return HttpResponse(json.dumps({"retcode": 0, "total": len(projectLists), "rows": data}))
    except:
        return HttpResponse(json.dumps({"retcode": -1,
                                        "total": 0,
                                        "rows": "",
                                        "msg": "查询出错！"}))


# 用例集维护
def testcase_list(request):
    project_list=Project_info.objects.filter(isdelete=0).values_list("pname")
    # template_info_list=Template_info.objects.filter(isdelete=0).values_list("id","pnumber__pname","templatename")
    data={
        'project_list': project_list,
        # 'template_info_list': template_info_list
    }
    if request.session.get('is_login', None):
        return render(request, "TestCasePage/testSuiteManagement.html", data)
    else:
        return redirect("/web/login")



# 新增用例集
def add(request):
    projectName=request.POST.get('projectName')
    templateName=request.POST.get('templateName')
    # print(request.POST.get('type'))
    if request.POST.get('type')=='1':
        project=Project_info.objects.get(pname=projectName)
        try:
            Template_info.objects.create(templatename=templateName,pnumber=project)
            return HttpResponse("添加成功！")
        except Exception as err:
            # print(err)
            return HttpResponse("添加时异常！")
    elif request.POST.get('type')=='0':
        temid=request.POST.get('temId')
        try:
            Template_info.objects.filter(id=temid).update(templatename=templateName)
            return HttpResponse("修改成功！")
        except Exception as err:
            # print(err)
            return HttpResponse("修改异常！")
    else:
        return HttpResponse("请求参数错误！")


# 删除用例集
def delete(request):
    templateId = request.POST.get('templateID')
    usercases=list(Template_detail.objects.filter(templateid=templateId, isdelete='0'))
    if len(usercases)>0:
        return HttpResponse(json.dumps({"retcode": "-1", "msg": "此用例集下还有用例，不能删除！"}))
    else:
        result=Template_info.objects.filter(id=templateId).update(isdelete=1)
        if result==1:
            return HttpResponse(json.dumps({"retcode": "0", "msg": "删除成功！"}))
        else:
            return HttpResponse(json.dumps({"retcode": "-2", "msg": "删除异常！"}))
