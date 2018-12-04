'''
作者：小华
描述：批量创建JOB
'''
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Test_Interface_Web.settings")
django.setup()
from DB.models import *
from apscheduler.schedulers.blocking import BlockingScheduler
import apscheduler
import datetime
from TestCaseManage import case_task_views
from utils.mail import Email
from utils.assertion import Jsonprint
import json
from django.db import connections
import logging
from StatisticsManage import views

logger = logging.getLogger("sourceDns.webdns.views")


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton,cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance


def close_old_connections():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()


def handle_db_connections(func):
    def func_wrapper(*args, **kwargs):
        close_old_connections()
        result = func(*args, **kwargs)
        close_old_connections()

        return result

    return func_wrapper


class Jobs(Singleton):
    def __init__(self):
        try:
            self.scheduler
        except Exception as e:
            logger.error('未能获取定时任务的创建计划，新建计划(第一次启动)'+str(e))
            self.scheduler=BlockingScheduler()
            self.scheduler.add_listener(my_listener, apscheduler.events.EVENT_JOB_EXECUTED | apscheduler.events.EVENT_JOB_ERROR)

    def addjob(self):
        # 查询JOB表
        lists = getjob_info()
        for i in range(0, len(lists)):
            caselist = lists[i]['caselist']
            day_of_week = lists[i]['day_of_week']
            runnertime = lists[i]['runnertime']
            jobid = lists[i]['jobid']
            runner_time = runnertime.split(':')
            mailaddress = lists[i]['mailaddress']
            jobcontent=lists[i]['jobcontent']
            jobtarget=lists[i]['jobtarget']

            # 添加JOB
            try:
                self.scheduler.add_job(func=runnerjob, args=(self.scheduler, caselist, mailaddress,jobcontent,jobtarget), trigger='cron',
                                       day_of_week=day_of_week, hour=str(runner_time[0]),
                                       minute=str(runner_time[1]), second=str(runner_time[2]), id=jobid)
            except Exception as e:
                logger.error('定时任务添加job异常'+str(e))
                pass

    # 开始JOB
    def startjob(self):
        try:
            self.scheduler.start()
        except Exception as e:
            logger.error('定时任务启动异常'+str(e))
            pass

    # 停止JOB
    def stopjob(self):
        try:
            self.scheduler.shutdown(wait=False)
        except apscheduler.schedulers.SchedulerNotRunningError as e:
            logger.error('定时任务停止异常'+str(e))
            pass


def my_listener(event):
    if event.exception:
        logger.error('The job %s crashed :(', str(event))
    else:
        logger.info('The job %s worked :)', str(event))


# 执行JOB
@handle_db_connections
def runnerjob(scheduler, id,mailaddress,jobcontent,jobtarget):
    logger.info('开始执行定时任务，用例集id是'+str(id))
    logger.info(str(scheduler.get_jobs()))
    # close_old_connections()
    #获取用例集ID
    case_list=list(Template_detail.objects.filter(templateid_id=id,isdelete=0).values('usercaseid_id','usercaseid__usercasename','usercaseid__isequal','usercaseid__isnotequal').order_by('usercaseid__run_order'))
    casecount=len(case_list)
    templatename=list(Template_info.objects.filter(id=id,isdelete=0).values('templatename','publicpar','pnumber'))    #用例集名称
    pubpar=templatename[0]['publicpar']    #公共参数
    if(pubpar!=None and pubpar!=""):
        pubpar=eval(pubpar)


    #添加测试报告
    okcount=0
    failcount=0
    errorcount=0
    r_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    obj=Interface_result(templateid_id=id,totalcount=casecount,okcount=okcount,failcount=failcount,errorcount=errorcount,runnertime=r_time)
    obj.save()
    objid=obj.id

    #执行用例集
    for i in range(0,casecount):
        caseid=case_list[i]["usercaseid_id"]
        casename=case_list[i]["usercaseid__usercasename"]
        isequal=case_list[i]["usercaseid__isequal"]
        isnotequal=case_list[i]["usercaseid__isnotequal"]
        actualdata=''


        #判断用例名字是否为空
        if casename!="":

            #检查点
            jp=Jsonprint()
            ttype=0     #检查状态
            try:
                r=case_task_views.run_case(caseid,pubpar)      #接口返回结果
                r_text=json.loads(r)            #JSON转字典
                r_result=r_text['msg']
                r_type=r_text['resulttype']   #结果状态
                actualdata=jp.show_real_data(r_text['actual_url'],r_text['actual_headers'],r_text['actual_data'])

                if r_type==200:

                    if isequal!='':
                        check_str=jp.checkresult(r_result,isequal,1)      #检查点内容
                    elif isnotequal!='':
                        check_str=jp.checkresult(r_result,isnotequal,2)      #检查点内容
                    else:
                        check_str=''
                    ttype=jp.resulttype     #检查状态
                else:
                    check_str=''
                    errorcount+=1
            except Exception as e:
                logger.error(caseid+casename+'执行失败！'+str(e))
                errorcount+=1
                check_str=''
                r_result=str(e)


            #计算通过数和失败数
            if ttype==1:
                okcount+=1
            elif ttype==2:
                failcount+=1

            #添加测试报告明细
            objlist=Interface_result_detail(resultid_id=objid,usercaseid_id=caseid,type=ttype,resultinfo=r_result,checkinfo=check_str,runnertime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),actualdata=actualdata)
            objlist.save()
            #修改通过数和失败数
            Interface_result.objects.filter(id=objid).update(okcount=okcount,failcount=failcount,errorcount=errorcount)

    #统计数据
    runnerstate=0
    if failcount==0 and errorcount==0:
        runnerstate=1
    views.saveresult(pnumber=templatename[0]['pnumber'],templateid=id,runnerstate=runnerstate,runnertime=r_time,okcount=okcount,failcount=failcount,errorcount=errorcount)


    #发邮件
    emailtitle='【'+templatename[0]['templatename']+'】接口自动化测试报告'
    _content = """
    <html>
        <body>
            <table>
                <tr>
                    <td><b>测试描述：</b></td>
                    <td style="text-align: left">%s</td>
                </tr>
            </table>
            <div>------------------------------------------------------------------------------------</div>
            <table>
                <tr>
                    <td><b>测试目标：</b></td>
                    <td style="text-align: left">%s</td>
                </tr>
            </table>
            <div>------------------------------------------------------------------------------------</div>
            <table>
                <tr>
                    <td><b>执行时间：</b></td>
                    <td>%s</td>
                </tr>
                <tr>
                    <td><b>用例总数：</b></td>
                    <td>%d个</td>
                </tr>
                <tr>
                    <td><b>通过数：</b></td>
                    <td>%d个</td>
                </tr>
                <tr>
                    <td><b>失败数：</b></td>
                    <td>%d个</td>
                </tr>
                <tr>
                    <td><b>错误数：</b></td>
                    <td>%d个</td>
                </tr>
                <tr>
                    <td><b>报告详情地址：</b></td>
                    <td><a href="http://10.9.2.142/report/testreport?id=%d" target="_blank">点击查看详情</a></td>
                </tr>
            </table>
        </body>
    </html>
    """%(jobcontent,jobtarget,r_time,casecount,okcount,failcount,errorcount,objid)

    e = Email(title=emailtitle,
                  message=_content,
                  receiver=mailaddress,
                  server='smtp.7lk.com',
                  sender='7lktest@7lk.com',
                  password='29De8lhGibAE59Qw',
                  path=''
                  )
    logger.info('开始发送邮件！')
    e.send()


#获取定时任务
def getjob_info():
    jblist=list(Job_info.objects.filter(isdelete=0,jobtype=0).values('id','jobid','mailaddress','day_of_week','runnertime','caselist','jobtype','jobcontent','jobtarget'))
    return jblist



if __name__=="__main__":
    runnerjob(66,'shilongzi@7lk.com',"123","45</br>6")
    #job=Jobs()
    #job.startjob()

