from TestCaseManage.case_task_views import run_case
from django.http.response import HttpResponse
import json
from utils.assertion import Jsonprint
from DB.models import *

"""
【带返回检查点执行用例入口】
    形参：request
    res:接口的response结果
"""
def start_run_checkcase(request):
    caseid = request.POST.get("caseid", 0)
    tempaleid = request.POST.get("templetid")#获取模板的ID

    # pubpar = eval(list(Template_info.objects.filter(id=tempaleid).values("publicpar"))[0].get("publicpar"))#获取功能参数
    pubpar = list(Template_info.objects.filter(id=tempaleid).values("publicpar"))[0].get("publicpar")#获取功能参数
    if(pubpar!=None and pubpar !=""):
        pubpar = eval(pubpar)
    # print("----",pubpar)
    usercase=list(User_case.objects.filter(id=caseid).values("isequal","isnotequal"))   #查找检查点
    isequal=usercase[0]['isequal']
    isnotequal=usercase[0]['isnotequal']


    jp=Jsonprint()
    check_isequal=''
    check_isnotequal=''
    # 3、获取用例详情
    r = run_case(caseid,pubpar)
    r_text=json.loads(r)            #JSON转字典
    r_result=r_text['msg']
    r_type=r_text['resulttype']   #结果状态
    r_url=r_text['actual_url']
    r_headers=r_text['actual_headers']
    r_data=r_text['actual_data']
    check_type=0       #检查点状态

    if r_type==200:
        if isequal!='':
            check_isequal=jp.checkresult(r_result,str(isequal),1)      #检查点内容
            if jp.resulttype==2:
                check_type=1

        if  isnotequal!='':
            check_isnotequal=jp.checkresult(r_result,str(isnotequal),2)      #检查点内容
            if jp.resulttype==2:
                check_type=1

    r_real_data = jp.show_real_data(r_url, r_headers, r_data)

    return HttpResponse(json.dumps({
        "msg": r_result,
        "resulttype":r_type,
        "r_data": r_real_data,
        "check_isequal":check_isequal,
        "check_isnotequal":check_isnotequal,
        "check_type":check_type}))