# coding=utf-8
from django.shortcuts import render, HttpResponse
from DB.models import *
from django.db.models import Count,Sum
import json
import datetime
from django.http import JsonResponse

# 获取项目名称,用例集
def statistics(request):
    #分组查询项目名称和项目ID
    prolist=Statistcs_info.objects.values('pnumber__pname','pnumber__pnumber')
    prolist.query.group_by = ['pnumber']
    #获取当前项目用例集ID
    if request.method=='POST':
        pid=request.POST.get("pid",None) #获取项目ID
        interfacetotal=Interface_info.objects.filter(pnumber=pid,isdelete=0).count()  #按项目ID查询接口总数
        usercasetotal=Template_detail.objects.filter(templateid__pnumber=pid,isdelete=0).count()  #按项目ID查询用例总数

        '''计算成功率'''
        starttime=Statistcs_info.objects.filter(pnumber=pid).values('runnertime').order_by('-runnertime')[:1]  #取最近日期
        start_time=datetime.datetime.strptime(starttime[0]['runnertime'], '%Y-%m-%d %H:%M:%S')  #初始时间
        sevendate=(start_time+datetime.timedelta(days=-7)).strftime('%Y-%m-%d %H:%M:%S')        #计算最近7天时间
        threedate=(start_time+datetime.timedelta(days=-30)).strftime('%Y-%m-%d %H:%M:%S')        #计算最近30天时间

        seventotal = Statistcs_info.objects .filter(pnumber=pid,runnertime__gt=sevendate).values('runnertime').count()  #查询最近7天时间总数
        sevencount = Statistcs_info.objects .filter(pnumber=pid,runnertime__gt=sevendate,runnerstate=1).values('runnertime').count()  #查询最近7天时间成功数

        threetotal=Statistcs_info.objects .filter(pnumber=pid,runnertime__gt=threedate).values('runnertime').count()  #查询最近30天时间总数
        threecount=Statistcs_info.objects .filter(pnumber=pid,runnertime__gt=threedate,runnerstate=1).values('runnertime').count()  #查询最近30天时间成功数

        servenpercent='{:.0f}'.format(sevencount/seventotal*100)
        noservenpercent=100-int(servenpercent)
        threepercent='{:.0f}'.format(threecount/threetotal*100)
        nothreepercent=100-int(threepercent)


        '''计算汇总报表'''
        t_id=Template_info.objects.filter(pnumber=pid,isdelete=0).values('id','templatename')
        aa=""
        bb={}
        for i in range(len(t_id)):
            bb['product']=t_id[i]['templatename']
            okcount=Statistcs_info.objects.filter(pnumber=pid,templateid=t_id[i]['id']).aggregate(Sum('okcount'))['okcount__sum']
            failcount=Statistcs_info.objects.filter(pnumber=pid,templateid=t_id[i]['id']).aggregate(Sum('failcount'))['failcount__sum']
            errorcount=Statistcs_info.objects.filter(pnumber=pid,templateid=t_id[i]['id']).aggregate(Sum('errorcount'))['errorcount__sum']

            if okcount==None:
                bb['通过数']=0
            else:
                bb['通过数']=okcount

            if failcount==None:
                bb['失败数']=0
            else:
                bb['失败数']=failcount

            if errorcount==None:
                bb['报错数']=0
            else:
                bb['报错数']=errorcount
            if okcount!=None and failcount!=None and errorcount!=None:
                aa+=str(bb)+','
        return HttpResponse(json.dumps({"msg":aa,
                                        'interfacetotal':interfacetotal,
                                        'usercasetotal':usercasetotal,
                                        'servenpercent':servenpercent,
                                        'noservenpercent':noservenpercent,
                                        'threepercent':threepercent,
                                        'nothreepercent':nothreepercent}))
    return render(request, 'StatisticsPage/statisticsinfo.html',{'project_info':prolist})

'''
保存统计结果
'''
def saveresult(pnumber,templateid,runnerstate,runnertime,okcount,failcount,errorcount):
    pnumber_id=Project_info.objects.get(pnumber=pnumber)
    t_id=Template_info.objects.get(id=templateid)
    obj=Statistcs_info(pnumber=pnumber_id,templateid=t_id,runnerstate=runnerstate,runnertime=runnertime,okcount=okcount,failcount=failcount,errorcount=errorcount)
    obj.save()