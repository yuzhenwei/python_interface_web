from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from DB.models  import *
import json,requests
from django.core import serializers
from utils.client import HTTPClient
from utils.assertion import Jsonprint
from utils.joinjson import JoinPar
import datetime
from StatisticsManage import views as sview

# 用例集维护
def testcase_maintain(request):
    project_info=Project_info.objects.filter(isdelete=0).order_by("pnumber")
    if request.method=='POST':
        btype=request.POST.get("btype",None) #获取业务ID
        if btype=="1":
            #读取用例集信息
            pro_id=request.POST.get("pro_id",None)
            template_info=list(Template_info.objects.filter(isdelete=0,pnumber=pro_id).values())
            return HttpResponse(json.dumps({"template_msg":template_info}))
        elif btype=="2":
            #读取接口模块
            pro_type=request.POST.get("pro_type",None)
            pro_model=list(Project_model.objects.filter(isdelete=0,pnumber=pro_type).values())
            return HttpResponse(json.dumps({"msg":pro_model}))
        elif btype=="3":
            #查询接口信息
            pro_model=request.POST.get("pro_model",None)
            pro_id=request.POST.get("pro_status",0)
            interface_name=request.POST.get("interface_name",None)
            if interface_name!="" and pro_model!="-1":
                interface_info=list(Interface_info.objects.filter(mnumber=pro_model,isdelete=0,interfacename=interface_name).values())
            elif pro_model=="-1" and interface_name=="":
                interface_info=list(Interface_info.objects.filter(pnumber=pro_id,isdelete=0).values())
            elif pro_model=="-1" and interface_name!="":
                interface_info=list(Interface_info.objects.filter(pnumber=pro_id,interfacename=interface_name,isdelete=0).values())
            else:
                interface_info=list(Interface_info.objects.filter(mnumber=pro_model,isdelete=0).values())
            return HttpResponse(json.dumps({"interface_info":interface_info}))
        elif btype=="4":
            interfaceid=request.POST.get("interfaceid",None)
            templateid=request.POST.get("templateid",None)
            #添加用例集明细
            obj=Template_detail(interfaceid_id=interfaceid,templateid_id=templateid,usercaseid_id=-1)
            obj.save()
            return HttpResponse(json.dumps({"addmsg":1}))
        elif btype=="5":
            #查询用例集
            template_id=request.POST.get("templateid",None)
            td=list(Template_detail.objects.filter(templateid_id=template_id,isdelete=0).
                    values("id","interfaceid__id","interfaceid__pname","interfaceid__mname",
                           "interfaceid__interfacename","interfaceid__url","interfaceid__defaultpar","interfaceid__type",
                           "usercaseid","templateid__templatename").order_by("-id"))
            #获取所有的用例集名称
            casetb=list(User_case.objects.filter(isdelete=0).values("id","usercasename"))
            return HttpResponse(json.dumps({"msg":td,"casemsg":casetb}))
        elif btype=="6":
            #添加用例
            case_name=request.POST.get("case_name",None)
            param_info=request.POST.get("param_info",None)
            interfaceid=request.POST.get("interfaceid",None)
            isequal=request.POST.get("isequal","")
            isnotequal=request.POST.get("isnotequal","")
            iscontain=request.POST.get("iscontain","")
            isnotcontain=request.POST.get("isnotcontain","")
            isheader=request.POST.get("isheader",0)
            headerinfo=request.POST.get("headerinfo","")
            isjoin=request.POST.get("isjoin",0)
            joininfo=request.POST.get("join_info","")

            caseobj=User_case(interfaceid_id=interfaceid,paraminfo=param_info,isequal=isequal,isnotequal=isnotequal,iscontain=iscontain,isnotcontain=isnotcontain,usercasename=case_name,isjoin=isjoin,isheader=isheader,headerinfo=headerinfo,joininfo=joininfo)
            caseobj.save()

            #修改用例集usercaseid
            templateid=request.POST.get("templateid",None)
            Template_detail.objects.filter(id=templateid).update(usercaseid_id=caseobj.id)
            return HttpResponse(json.dumps({"addmsg":1}))
        elif btype=="8":
            #查询关联用例集
            template_id=request.POST.get("t_id",None)
            casename=request.POST.get("casename","")
            if casename!="":
                td=list(Template_detail.objects.filter(usercaseid__usercasename=casename,templateid_id=template_id,usercaseid_id__gt=0).values("interfaceid__id","id","interfaceid__interfacename","usercaseid__usercasename","usercaseid").order_by("-id"))
            else:
                td=list(Template_detail.objects.filter(templateid_id=template_id,usercaseid_id__gt=0).values("interfaceid__id","id","interfaceid__interfacename","usercaseid__usercasename","usercaseid").order_by("-id"))
            return HttpResponse(json.dumps({"msg":td}))
        elif btype=="9":
            #获取默认用例集
            template_id=request.POST.get("t_id",None)
            td=list(Template_detail.objects.filter(templateid_id=template_id,usercaseid_id__gt=0,isdelete=0).values("interfaceid__id","id","interfaceid__interfacename","usercaseid__usercasename","usercaseid").order_by("-id"))

            #读取编辑用例
            caseid=request.POST.get("caseid",None)
            caseinfo=list(User_case.objects.filter(id=caseid,isdelete=0).values("paraminfo","isequal","isnotequal","iscontain",
                                                                                "isnotcontain","usercasename","isjoin","joininfo",
                                                                                "isheader","headerinfo","rejoin_key","run_order","interfaceurl"))
            return HttpResponse(json.dumps({"case_infomsg":caseinfo,"msg2":td}))
        elif btype=="11":
            #查询编辑关联用例集
            template_id=request.POST.get("t_id",None)
            casename=request.POST.get("casename","")
            if casename!="":
                td=list(Template_detail.objects.filter(usercaseid__usercasename=casename,templateid_id=template_id,usercaseid_id__gt=0).values("interfaceid__id","id","interfaceid__interfacename","usercaseid__usercasename","usercaseid").order_by("-id"))
            else:
                td=list(Template_detail.objects.filter(templateid_id=template_id,usercaseid_id__gt=0).values("interfaceid__id","id","interfaceid__interfacename","usercaseid__usercasename","usercaseid").order_by("-id"))
            return HttpResponse(json.dumps({"msg2":td}))
        elif btype=="12":
            #保存编辑内容
            case_name=request.POST.get("case_name",None)
            param_info=request.POST.get("param_info",None)
            isequal=request.POST.get("isequal","")
            isnotequal=request.POST.get("isnotequal","")
            iscontain=request.POST.get("iscontain","")
            isnotcontain=request.POST.get("isnotcontain","")
            isheader=request.POST.get("isheader",0)
            headerinfo=request.POST.get("headerinfo","")
            isjoin=request.POST.get("isjoin",0)
            joininfo=request.POST.get("join_info","")
            upcase_id=request.POST.get("upcase_id",None)

            User_case.objects.filter(id=upcase_id).update(paraminfo=param_info,isequal=isequal,isnotequal=isnotequal,iscontain=iscontain,isnotcontain=isnotcontain,usercasename=case_name,isjoin=isjoin,isheader=isheader,headerinfo=headerinfo,joininfo=joininfo)
            return HttpResponse(json.dumps({"msg":"1"}))
        elif btype=="13":
            #删除用例集详情
            id=request.POST.get("id",None)
            Template_detail.objects.filter(id=id).update(isdelete=1)
            return HttpResponse(json.dumps({"msg":"1"}))
    return render(request,"TestCasePage/testcase_maintain.html",{"project_info":project_info})


#日期转码
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)


# 用例集维护
def testcase_info(request):
    if request.session.get('is_login', None):
        return render(request, "TestCasePage/testcase_info.html")
    else:
        return redirect("/web/login")


#执行接口
def testcaserunner(request):
    project_info=Project_info.objects.filter(isdelete=0).order_by("pnumber")
    if request.method=='POST':
        btype=request.POST.get("btype",None) #获取业务ID
        #绑定用例集下拉框
        if btype=="1":
            proid=request.POST.get("proid",None)     #获取项目ID
            template_info=list(Template_info.objects.filter(isdelete=0,pnumber=proid).values("templatename","id"))
            return HttpResponse(json.dumps({"template_msg":template_info}))
        #查询用例--根据查询结果渲染表格
        elif btype=="2":
            templateid=request.POST.get("templateid",0)
            caseinfo=list(Template_detail.objects.filter(templateid_id=templateid, isdelete=0, usercaseid_id__gt=0
                                                         ).exclude(usercaseid__usercasename="").order_by(
                "usercaseid__run_order").values("usercaseid_id", "id", "templateid__id", "interfaceid__interfacename",
                                                "usercaseid__usercasename", "usercaseid__isequal",
                                                "usercaseid__iscontain", "usercaseid__isnotcontain",
                                                "usercaseid__isnotequal", "usercaseid__interfaceurl",
                                                "usercaseid__paraminfo"))

            return HttpResponse(json.dumps({"caseinfo":caseinfo}))
        #执行接口
        elif btype=="3":
            caseid=request.POST.get("caseid",0)
            case_list=list(User_case.objects.filter(id=caseid).values("interfaceid__url","isheader","headerinfo","paraminfo","isjoin","joininfo","interfaceid__type"))
            #读取用例信息
            case_url=case_list[0]["interfaceid__url"]             #url
            case_type=case_list[0]["interfaceid__type"]           #接口类型
            if case_type==1:
                casetype="POST"
            else:
                casetype="GET"
            case_par=case_list[0]["paraminfo"].replace(' ','')      #参数
            isheader=case_list[0]["isheader"]         #是否头部
            if isheader==1:
                headerinfo=case_list[0]["headerinfo"].replace(' ','')    #头部信息
            else:
                headerinfo=None
            isjoin=case_list[0]["isjoin"]             #是否关联
            joininfo=case_list[0]["joininfo"]         #关联信息

            header_top_from="application/x-www-form-urlencoded"
            header_top_json ="application/json"

            #执行接口
            if isjoin==1:
                join_info=eval(joininfo)
                joinparam={}
                for j in range(len(join_info)):
                    caseid=join_info[j]["caseid"]
                    #根据caseID读取用例信息
                    case_info=list(User_case.objects.filter(id=caseid).values("interfaceid__url","interfaceid__type","paraminfo","isheader","headerinfo"))
                    url=case_info[0]["interfaceid__url"]
                    m_type=case_info[0]["interfaceid__type"]
                    if m_type==1:
                        c_type="POST"
                    else:
                        c_type="GET"
                    paraminfo=case_info[0]["paraminfo"].replace(' ','')
                    isheader=case_info[0]["isheader"]         #是否头部
                    if isheader==1:
                        headerinfo_l=case_info[0]["headerinfo"]     #头部信息
                    else:
                        headerinfo_l=None

                    jsonpar = join_info[j]["jsonpar"].split(';')

                    # 接口关联:是修改指定的入参替换用例中的值
                    global null
                    global true, false
                    null = ''
                    true = "'true'"
                    false = "'false'"
                    case_par = eval(case_par)  # 修改入参类型为dict
                    for jpar in jsonpar:
                        qw = jpar.split("=")
                        pr_key=qw[0] #入参中的key
                        pr_val=qw[1]  #需要依赖的key
                        if(headerinfo_l == None):
                            r, _, _, _ = HTTPClient(url=url, method=c_type, headers=headerinfo_l).send(data=eval(paraminfo))  # 执行关联接口
                        elif(header_top_from in headerinfo_l):
                            r, _, _, _ = HTTPClient(url=url, method=c_type, headers=eval(headerinfo_l)).send(data=eval(paraminfo))
                            # r = requests.post(url=url,headers=eval(headerinfo_l),data=eval(paraminfo))
                        elif(header_top_json in headerinfo_l):
                            r, _, _, _ = HTTPClient(url=url, method=c_type, headers=headerinfo_l).send(params=eval(paraminfo))  # 执行关联接口
                            #print("执行关联接口——", headerinfo_l, paraminfo, r.text)
                        jp = JoinPar()  # 提取关联接口结果参数
                        jp.print_json_key(eval(r.text),pr_val)
                        #case_par[pr_key]=jp.key_info[pr_val]
                        replace_val = jp.key_info[pr_val]
                        case_par=jp.key_replace_value(case_par,pr_key,replace_val)#关联接口替换

                    #print("new----",case_par)
                    # joinparam = dict(joinparam, **jp.key_info)  # 合并提取参数

                    # for jpar in jsonpar:
                    #     r=HTTPClient(url=url, method=c_type,headers=headerinfo).send(data=eval(paraminfo))        #执行关联接口
                    #     jp=JoinPar()                #提取关联接口结果参数
                    #     jp.print_json_key(eval(r.text),jpar)
                    #     joinparam=dict(joinparam,**jp.key_info)     #合并提取参数

                    #原有参数合并
                    # newpar=dict(eval(case_par),**joinparam)


                    try:

                        if (headerinfo == None):
                            r, _, _, _ = HTTPClient(url=case_url, method=casetype, headers=headerinfo).send(data=case_par)
                        elif (header_top_from in headerinfo):
                            r, _, _, _ = HTTPClient(url=case_url, method=casetype, headers=eval(headerinfo)).send(data=case_par)
                            # r = requests.post(url=case_url, headers=eval(headerinfo), data=case_par)
                            # print("+",case_url, headerinfo, case_par)
                            # print("------",r.text)
                        elif (header_top_json in headerinfo):
                            r, _, _, _ = HTTPClient(url=case_url, method=casetype, headers=headerinfo).send(params=case_par)
                        #r=HTTPClient(url=case_url, method=casetype,headers=headerinfo).send(data=case_par)
                        resulttype=r.status_code

                        return HttpResponse(json.dumps({"msg":r.text,"resulttype":resulttype}))
                    except Exception as e:
                        return HttpResponse(json.dumps({"msg":e,"resulttype":"110"}))


            else:
                # 如果不是关联用例执行以下代码，请求头不为None时，执行
                try:
                    if (headerinfo == None):
                        r, _, _, _ = HTTPClient(url=case_url, method=casetype, headers=headerinfo).send(data=eval(case_par))
                    elif (header_top_from in headerinfo):
                        r, _, _, _ = requests.post(url=case_url,headers=eval(headerinfo),data=eval(case_par))

                    elif (header_top_json in headerinfo):
                        r, _, _, _ = HTTPClient(url=case_url, method=casetype,headers=headerinfo).send(params=eval(case_par))
                    resulttype=r.status_code
                    # print(r.text)
                    return HttpResponse(json.dumps({"msg":r.text,"resulttype":resulttype}))
                except Exception as e:
                    return HttpResponse(json.dumps({"msg":e,"resulttype":"110"}))
        elif btype=="4":
            #生成测试报告
            result_list=eval(request.POST.get("result_list",None))
            t_id=int(result_list["templateid"])
            totalcount=result_list["totalcount"]
            okcount=result_list["okcount"]
            failcount=result_list["failcount"]
            errorcount=result_list["errorcount"]
            runnertime=result_list["runnertime"]
            runnertime=datetime.datetime.strptime(runnertime,"%Y-%m-%d %H:%M:%S")
            pnumber=int(result_list['pnumber'])
            obj=Interface_result(templateid_id=t_id,totalcount=totalcount,okcount=okcount,failcount=failcount,errorcount=errorcount,runnertime=runnertime)
            obj.save()

            #统计数据
            runnerstate=0
            if failcount==0 and errorcount==0:
                runnerstate=1
            sview.saveresult(pnumber=pnumber,templateid=t_id,runnerstate=runnerstate,runnertime=runnertime,okcount=okcount,failcount=failcount,errorcount=errorcount)

            return HttpResponse(json.dumps({"msg":obj.id}))
        elif btype=="5":
            # 测试报告明细
            resultdetail = eval(request.POST.get("resultdetail",""))
            for i in range(len(resultdetail)):
                resultid = int(resultdetail[i]["resultid"])
                ttype = resultdetail[i]["type"]
                resultinfo = resultdetail[i]["resultinfo"]
                checkinfo = resultdetail[i]["checkinfo"]
                actual_data = resultdetail[i]["actual_data"]
                caseid = resultdetail[i]["caseid"]

                objlist = Interface_result_detail(resultid_id=resultid,usercaseid_id=caseid,type=ttype,resultinfo=resultinfo,checkinfo=checkinfo,actualdata=actual_data,runnertime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                objlist.save()
            return HttpResponse(json.dumps({"msg":"1"}))
        elif btype == "6":
            #读取测试报告
            tid=request.POST.get("templateid",None)   #用例集ID
            #print(tid)
            template_result = list(Interface_result.objects.filter(templateid__id=tid,isdelete=0).values("templateid__id","id","templateid__pnumber__pname","templateid__templatename","okcount","errorcount","failcount","totalcount","runnertime").order_by("-runnertime"))
            #print(template_result)
            return HttpResponse(json.dumps({"reportinfo":template_result},cls=DateEncoder))

    return render(request, "TestCasePage/testcaserunner.html", {"project_info" : project_info})

