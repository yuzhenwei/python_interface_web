from django.shortcuts import render, redirect, HttpResponse
import json, requests,ast
from DB.models import *
from utils.client import HTTPClient
from utils.HttpClass import  HttpRequest
from utils.assertion import Jsonprint
"""
"code":   0                 -1,"msg": "请求方法传递错误！"
"retcode":0, "msg": "成功！" -1 "msg":"requests请求出错！"
"""

def main(request):
    pro_content = list(Project_info.objects.all().values("pname", "pnumber"))
    if request.session.get('is_login', None):
        return render(request, "InterfacePage/quicktest.html", locals())
    else:
        return redirect("/web/login")



# 运行接口函数
def run_interface(request):
    if request.method == 'POST':
        btype = request.POST.get("btype", None)  # 获取业务ID
        # 执行接口
        if btype == "1":
            url = request.POST.get("interface_url", None)
            interface_method = request.POST.get("interface_method", None)

            headers = request.POST.get("headers", None)

            headers = ast.literal_eval(headers)
            param = request.POST.get("param", None)

            if interface_method == '1':
                interface_method = "POST"
                data = json.loads(param)

            elif interface_method == '0':
                interface_method = "GET"
                if(param==None or param==""):
                    pass
                else:
                    url=url+'?'+param
            else:
                return HttpResponse(json.dumps({"code":-1,"msg": "请求方法传递错误！", "resulttype": "0"}))

            try:
                if interface_method== "GET":
                    r, _, _, _ = HttpRequest(url=url, method=interface_method,headers=headers).send()
                    #r = HTTPClient(url=url, method=interface_method).send()
                else:
                    if headers['Content-Type']=="application/json":
                        #r = HTTPClient(url=url, method=interface_method, headers=headers).send(params=data)
                        r, _, _, _ = HttpRequest(url=url, method=interface_method,headers=headers).send(json_data=data)
                    else:
                        r, _, _, _ = HttpRequest(url=url, method=interface_method, headers=headers).send(form_data=data)

                resulttype = r.status_code

                #检查点
                checkequal_info=''
                checknotequal_info=''

                checkequal = request.POST.get("checkequal", '')  # 获取等于检查点
                checknotequal=request.POST.get("checknotequal",'')  #获取不等于检查点


                js=Jsonprint()
                if checkequal!='':
                    checkequal_info=js.checkresult(r.text,str(checkequal),1)

                if checknotequal!='':
                    checknotequal_info=js.checkresult(r.text,str(checknotequal),2)

                return HttpResponse(json.dumps({"retcode":0, "msg": r.text, "resulttype": resulttype,"checkequal_info":checkequal_info,"checknotequal_info":checknotequal_info}))
            except Exception as e:
                return HttpResponse(json.dumps({"retcode":-1, "msg":"requests请求出错！", "errorinfo": e, "resulttype": "0"}))

    return render(request, 'InterfacePage/quicktest.html')
