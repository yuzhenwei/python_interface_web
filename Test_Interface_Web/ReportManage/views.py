# coding=utf-8
from django.shortcuts import render, HttpResponse
from DB.models import *
import json
import datetime


# 获取项目名称,用例集
def report(request):
    # 初始化项目信息
    prolist = Project_info.objects.filter(isdelete=0).values("pname", "pnumber")
    if request.method=='POST':
        btype = request.POST.get("btype", None)
        # 根据项目查询用例集
        if btype == "1":
            pnumber = request.POST.get("pro",None)
            uselist = list(Template_info.objects.filter(isdelete=0,pnumber=pnumber).values("id","templatename","pnumber"))
            return HttpResponse(json.dumps({"msglist": uselist}))
        elif btype == "2":
            # 根据用例集查询测试报告
            templateid = request.POST.get("templateid", None)
            offset = request.POST.get('offset')
            limit = request.POST.get('limit')
            try:
                result_list = list(Interface_result.objects.filter(templateid__id=templateid, isdelete=0).values(
                    "templateid__id", "id", "templateid__pnumber__pname", "templateid__templatename", "okcount",
                    "errorcount", "failcount", "totalcount", "runnertime").order_by("-runnertime"))
                result_info = result_list[int(offset):int(limit)+int(offset)]
                return HttpResponse(json.dumps({"retcode": 0,
                                                "msglist": result_info,
                                                "total": len(result_list),
                                                "rows": result_info}, cls=DateEncoder))
            except:
                return HttpResponse(json.dumps({"retcode": -1,
                                     "msg": "查询出错！"}))
    return render(request, 'ReportPage/report.html', locals())


# 查看测试报告
def interfaceresult(request):
    # 初始化数据
    id = request.GET['id']
    resultinfo = Interface_result.objects.filter(id=id).values("templateid__templatename", "totalcount", "okcount",
                                                             "failcount", "errorcount", "runnertime", "runnertime", "id")
    resultdetail = Interface_result_detail.objects.filter(resultid__id=resultinfo[0]["id"]).values("id",
                                                                                                 "usercaseid__interfaceid__interfacename", "usercaseid__usercasename", "usercaseid__interfaceurl",
                                                                                                 "type", "failinfo", "resultinfo", "checkinfo", "versionnum", "runnertime","actualdata")
    return render(request, 'ReportPage/interfaceresult.html', {'modelname':resultinfo[0]["templateid__templatename"],
                                                               'runnertime':str(resultinfo[0]["runnertime"]),
                                                               'totalcount':resultinfo[0]["totalcount"],
                                                               'okcount':resultinfo[0]["okcount"],
                                                               'failcount':resultinfo[0]["failcount"],
                                                               'errorcount':resultinfo[0]["errorcount"],
                                                               'resultdetail':resultdetail})


#日期转码
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)
