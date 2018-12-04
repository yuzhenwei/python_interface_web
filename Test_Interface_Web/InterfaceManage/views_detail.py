from django.shortcuts import render,redirect,HttpResponse
import json
from math import ceil
from DB.models  import  *

"""查询接口详细信息"""
def interfaceDetail(request):
    interfaceId=request.POST.get("id")
    # print(interfaceId)
    detail = Interface_info.objects.filter(id=interfaceId,isdelete=0).values("id", "interfacename", "url", "defaultpar",
                                                                                     "type", "mname", "remark","pnumber_id","mnumber").order_by('-id')
    # print(detail)
    # return render(request,'InterfacePage/interface_list.html',{'list':detail})
    return HttpResponse(json.dumps({"msg":list(detail)}))