from django.db import models
# Create your models here.

#用户表的信息
class User_info(models.Model):
    username=models.CharField("名称",max_length=30)
    password=models.CharField("密码",max_length=50)
    name = models.CharField("姓名", max_length=50)
    isdelete=models.IntegerField("是否删除",default=0)
    class Meta:
        db_table = 'user_info'#指定数据表的名称

#项目表（project_info）
class Project_info(models.Model):
    pname=models.CharField("项目名称",max_length=100)          #项目名称
    pnumber=models.BigAutoField("项目标识",max_length=100,primary_key=True)        #项目标识码
    description=models.CharField("项目描述",max_length=200)    #项目描述
    sortnum=models.IntegerField("项目排序号",default=0)                   #项目排序号
    isdelete=models.IntegerField(default=0)         #是否删除
    class Meta:
        db_table = 'project_info'  # 指定数据表的名称


#项目模块（project_model）
class Project_model(models.Model):
    pnumber=models.ForeignKey("Project_info")     #项目标识码（与项目表Pnumber关联）
    modelname=models.CharField("模块名称",max_length=100)      #模块名称
    mnumber=models.BigAutoField("模块标识号",max_length=100,primary_key=True)        #模块标识号
    description=models.CharField("模块描述",max_length=200)    #模块描述
    sortnum=models.IntegerField("模块排序号",default=0)                   #模块排序号
    isdelete=models.IntegerField("是否删除",default=0)         #是否删除
    class Meta:
        db_table = 'project_model'


# 接口表（interface_info）
class Interface_info(models.Model):
    interfacename = models.CharField("接口名称",max_length=100)  # 接口名称
    url = models.CharField("接口地址",max_length=500)  # 接口地址
    defaultpar = models.CharField("默认入参",max_length=10000)  # 默认入参
    remark = models.CharField("备注",max_length=100)  # 备注
    type = models.IntegerField()  # 接口类型'0为get  1为post'
    mnumber = models.ForeignKey("Project_model")  # 模块标识号（与模块表mnumber关联）
    pnumber =models.ForeignKey("Project_info") # 项目表的pnumber(与项目表pnumber关联）
    pname = models.CharField("项目名称",max_length=100)
    mname =models.CharField("模块名称",max_length=100)
    isdelete = models.IntegerField(default=0)  # 是否删除
    class Meta:
        db_table='interface_info'

# 用例表（usercase）
class User_case(models.Model):
    interfaceid = models.ForeignKey("Interface_info")  # 接口ID（与接口表interface_info  ID关联）
    interfaceurl = models.CharField("接口地址",max_length=500)  # 参数字段内容
    paraminfo = models.CharField("参数字段内容",max_length=10000)  # 参数字段内容
    isequal = models.CharField("是否等于",max_length=500)  # 是否等于
    isnotequal = models.CharField("是否不等于",max_length=500)  # 是否不等于
    iscontain = models.CharField("是否包含",max_length=500)  # 是否包含
    isnotcontain = models.CharField("不包含",max_length=500)  # 不包含
    usercasename = models.CharField("用例名称",max_length=100)  # 用例名称
    isjoin = models.IntegerField("是否关联",default=0)  # 是否关联（1是关联，0默认不关联）
    joininfo = models.CharField("关联描述",max_length=500)  # 关联内容
    rejoin_key = models.CharField("对外提供的关联key", max_length=500,null=True)  # 对外提供的关联值
    rejoin_value = models.CharField("对外提供的关联values",max_length=500,null=True)  # 对外提供的关联值
    isheader = models.IntegerField("是否有头部",default=0)  # 是否有头部（1是，0默认不是）
    headerinfo = models.CharField("Header内容",max_length=500)  # Header内容
    status = models.IntegerField("执行状态",default=0)  # 关联内容，0表示未执行，1表示已执行
    isdelete = models.IntegerField("是否删除",default=0)  # 是否删除
    run_order = models.IntegerField("执行顺序",default=-1) #执行顺序
    class Meta:
        db_table='user_case'


# 接口模板表（template_info）
class Template_info(models.Model):
    templatename = models.CharField("模板名称",max_length=100)  # 模板名称
    remark = models.CharField("备注",max_length=100)  # 备注
    isdelete = models.IntegerField("是否删除",default=0)  # 是否删除
    pnumber = models.ForeignKey("Project_info")  # 项目标识码（与项目表Pnumber关联）
    publicpar=models.CharField("公共参数",max_length=1000)  #公共参数
    class Meta:
        db_table='template_info'

# 接口模板明细表（template_detail）
class Template_detail(models.Model):
    templateid = models.ForeignKey("Template_info")  # 模板ID（与接口模板表template_info  ID关联）
    interfaceid = models.ForeignKey("Interface_info")  # 接口ID（与接口表interface_info  ID关联）
    usercaseid = models.ForeignKey("User_case")  # 用例ID（与模板参数表usercase ID关联）
    isdelete = models.IntegerField(default=0)  # 是否删除
    class Meta:
        db_table = 'template_detail'

#模板运行结果表（interface_result）
class Interface_result(models.Model):
    templateid=models.ForeignKey("Template_info")        #模板ID
    totalcount=models.IntegerField("用例总数",default=0)            #用例总数（默认0）
    okcount=models.IntegerField("通过数",default=0)                 #通过数（默认0）
    failcount=models.IntegerField("失败数",default=0)               #失败数（默认0）
    errorcount=models.IntegerField("错误数",default=0)              #错误数（默认0）
    runnertime=models.DateTimeField("运行时间",auto_now=True)      #运行时间（获取当前时间）
    isdelete=models.IntegerField("是否删除",default=0)              #是否删除
    class Meta:
        db_table = 'interface_result'

#模板运行结果明细表（interfaceresultdetail）
class Interface_result_detail(models.Model):
    resultid=models.ForeignKey("Interface_result")         #结果ID（与模板运行结果表interface_result ID关联）
    usercaseid=models.ForeignKey("User_case")              #用例ID(与用例表usercase id关联)
    type=models.IntegerField("结果类型")                          #结果类型'1通过  2失败  0错误
    failinfo=models.CharField("失败原因",max_length=500)           #失败原因
    resultinfo=models.TextField("json结果",max_length=500)         #json结果
    checkinfo=models.TextField("检查点结果",max_length=500)         #检查点结果
    actualdata=models.TextField("实际请求参数", max_length=12000)  # 实际请求参数
    versionnum=models.CharField("版本号",max_length=100)         #版本号
    runnertime=models.DateTimeField("运行时间",auto_now=True)      #运行时间（获取当前时间）
    class Meta:
        db_table='interface_result_detail'


#定时任务表（job_info）
class Job_info(models.Model):
    jobname=models.CharField("任务名称",max_length=100)           #任务名称
    jobid=models.CharField("定时任务ID",max_length=100)           #定时任务ID
    mailaddress=models.CharField("指向邮件地址",max_length=100)   #指向邮件地址
    day_of_week=models.CharField("运行时间段",max_length=100)      #运行时间段
    runnertime=models.CharField("执行时间",max_length=100)          #执行时间
    caselist=models.CharField("用例集",max_length=500)                 #用例集
    jobtype=models.IntegerField("状态",default=0)                  #状态  0为正常,1为暂停
    jobcontent=models.CharField("Job描述",max_length=1000)         #测试描述
    jobtarget = models.CharField("Job目标", max_length=1000)       #目标，目的
    isdelete=models.IntegerField("是否删除",default=0)             #是否删除
    class Meta:
        db_table = 'job_info'

#统计报表（statistcs_info）
class Statistcs_info(models.Model):
    pnumber =models.ForeignKey("Project_info") # 项目表的pnumber(与项目表pnumber关联）
    templateid=models.ForeignKey("Template_info")        #模板ID
    runnerstate=models.IntegerField("运行状态",default=0)   #运行状态，0为错误  1为正常  2为失败
    runnertime=models.CharField("执行时间",max_length=100)          #执行时间
    okcount=models.IntegerField("通过数",default=0)                 #通过数（默认0）
    failcount=models.IntegerField("失败数",default=0)               #失败数（默认0）
    errorcount=models.IntegerField("错误数",default=0)              #错误数（默认0）
    class Meta:
        db_table = 'statistcs_info'





















