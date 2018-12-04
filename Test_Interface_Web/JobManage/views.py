#coding=utf-8
from django.shortcuts import render,HttpResponse
from DB.models  import  *
import json
import datetime
from JobManage.run_jobs import Jobs
import os
import logging


logger = logging.getLogger("sourceDns.webdns.views")


#获取项目名称,用例集
def job(request):
    jblist=list(Job_info.objects.filter(isdelete=0).values('id','jobid','mailaddress','day_of_week','runnertime','caselist','jobtype','jobname','jobcontent','jobtarget'))      #获取任务
    prolist=list(Project_info.objects.filter(isdelete=0).values('pnumber','pname'))         #获取项目
    case_list=list(Template_info.objects.filter(isdelete=0).values('id','templatename'))        #获取用例集
    if request.method=='POST':
        btype=request.POST.get("btype",None)
        #根据项目查询用例集
        if btype=="1":
            proid=request.POST.get("proid",None)     #获取项目ID
            template_info=list(Template_info.objects.filter(isdelete=0,pnumber=proid).values("templatename","id"))
            return HttpResponse(json.dumps({"template_msg":template_info}))
        #添加任务
        elif btype=="2":
            job_name=request.POST.get("job_name",None)     #任务ID
            mail=request.POST.get("mail",None)     #邮件
            day_of_week=request.POST.get("day_of_week",None)     #时间段
            runnertime=request.POST.get("runnertime",None)     #运行时间
            jobtype=request.POST.get("jobtype",None)     #任务类型
            caseinfo=request.POST.get("caseinfo",None)     #用例集ID
            jobcontent=request.POST.get("jobcontent","")    #JOB描述
            jobtarget=request.POST.get("jobtarget","")      #JOB目标

            obj=Job_info(jobname=job_name,mailaddress=mail,day_of_week=day_of_week,runnertime=runnertime,jobtype=jobtype,caselist=caseinfo,jobcontent=jobcontent,jobtarget=jobtarget)
            obj.save()

            #修改ID
            job_id='task'+str(obj.id)
            Job_info.objects.filter(id=obj.id).update(jobid=job_id)

            return HttpResponse(json.dumps({"msg":"1"}))
        #查询和刷新页面
        elif btype=="3":
            jobkey=request.POST.get("jobkey","")     #任务名称
            if(jobkey!=""):
                jblist=list(Job_info.objects.filter(isdelete=0,jobname=jobkey).values('id','jobid','mailaddress','day_of_week','runnertime','caselist','jobtype','jobname','jobcontent','jobtarget'))
            else:
                jblist=list(Job_info.objects.filter(isdelete=0).values('id','jobid','mailaddress','day_of_week','runnertime','caselist','jobtype','jobname','jobcontent','jobtarget'))
            return HttpResponse(json.dumps({"msg":jblist}))
        #开启定时任务
        elif btype=="4":
            jb=Jobs()
            logger.info(str(jb)+str(jb.scheduler))

            try:
                if jb.scheduler.state:
                    logger.info(str(jb.scheduler.state) + "重启，之前已启动")
                    jblists=jb.scheduler.get_jobs()
                    for i in jblists:
                        jb.scheduler.remove_job(i.id)
                    jb.addjob()
                    logger.info('目前任务列表有' + str(jb.scheduler.get_jobs()))
                else:
                    logger.info(str(jb.scheduler.state) + "第一次启动，之前未启动")
                    jb.addjob()
                    logger.info('目前任务列表有' + str(jb.scheduler.get_jobs()))
                    jb.startjob()
            except Exception as e:
                errorinfo="启动失败，失败原因："+str(e)
                return HttpResponse(json.dumps({"msg":errorinfo}))
        #编辑定时任务
        elif btype=="5":
            j_id=request.POST.get("id",0)        #ID
            job_name=request.POST.get("job_name",None)     #任务名称
            mail=request.POST.get("mail",None)     #邮件
            day_of_week=request.POST.get("day_of_week",None)     #时间段
            runnertime=request.POST.get("runnertime",None)     #运行时间
            jobtype=request.POST.get("jobtype",0)     #任务类型
            jobcontent=request.POST.get("jobcontent","")    #JOB描述
            jobtarget=request.POST.get("jobtarget","")      #JOB目标

            '''
            print(j_id)
            print(job_id)
            print(mail)
            print(day_of_week)
            print(runnertime)
            print(jobtype)
            '''

            Job_info.objects.filter(id=j_id).update(jobname=job_name,mailaddress=mail,day_of_week=day_of_week,runnertime=runnertime,jobtype=jobtype,jobcontent=jobcontent,jobtarget=jobtarget)
            return HttpResponse(json.dumps({"msg":"1"}))
        #删除定时任务
        elif btype=="6":
            id=request.POST.get("id",0)     #ID
            Job_info.objects.filter(id=id).update(isdelete=1)
            return HttpResponse(json.dumps({"msg":"1"}))
    return render(request,'JobPage/jobinfo.html',{'jblist':jblist,'prolist':prolist,'case_list':case_list})












