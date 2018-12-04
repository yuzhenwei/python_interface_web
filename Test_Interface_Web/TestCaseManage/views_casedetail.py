# -*- coding:utf-8 -*

from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from DB.models  import *
import json
"""
查询用例的详细信息
"""
def casedetail(request):
    caseid=request.POST.get("id",None)
    # print(caseid)
    if caseid:
        try:
            # td=Template_detail.objects.filter(usercaseid=caseid,isdelete=0).values("interfaceid__remark","usercaseid__paraminfo","interfaceid__type",
            #                                                                                  "usercaseid__rejoin_key").order_by("-usercaseid")
            td=Template_detail.objects.filter(usercaseid=caseid,isdelete=0).values("usercaseid__id","interfaceid__id", "interfaceid__interfacename","usercaseid__usercasename",
                                                                                   "usercaseid__paraminfo","interfaceid__type","usercaseid","templateid__templatename","usercaseid__rejoin_key").order_by("-usercaseid__id")
            return HttpResponse(json.dumps({"retcode":0,"msg":list(td)}))
        except:
            return HttpResponse(json.dumps({"retcode":-1,"msg":"数据获取失败 ！"}))
    else:
        return HttpResponse(json.dumps({"code":-2,"msg":"请求参数错误！"}))
