from DB.models import *
from django.http import StreamingHttpResponse
from django.http.response import HttpResponse
from django.utils.encoding import escape_uri_path
import xlrd,operator,os,json
from xlutils.copy import copy
from django.db.models import Q
# def validate_excel(value):
#     if value.name.split('.')[-1] not in ['xls','xlsx']:
#         raise ValidationError(_('Invalid File Type: %(value)s'),params={'value': value},)

# class UploadExcelForm(forms.Form):
#  excel = forms.FileField(validators=[validate_excel]) #这里使用自定义的验证
"""
[上传接口模板]
作者：代代花
描述：接口页面中的导入调取此接口，只有在模板头相同的情况下才允许导入
response：成功返回“OK”,失败返回“Fail”
"""
def upload_inter(request):
    wb = xlrd.open_workbook(filename=None, file_contents=request.FILES['file'].read())  # 读取excel文件
    table = wb.sheets()[0]
    row = table.nrows #总行数
    table_header=['项目名称','模块名称','接口名称','URL','请求方式','参数','描述']
    #判断模板是否正确，通过operator.eq() 比较两个list是否相等
    if(operator.eq(table_header,table.row_values(0))):
        if(is_all_inter(table,row) == True):
            for i in range(1, row):#获取每一行的数据
                cel = table.row_values(i)
                for c in range(len(cel)):
                    cel[c] = cel[c].replace(' ', '')#去除空格
                #1、添加接口用例
                #2、获取项目ID
                if(cel[4].upper() =="POST"):
                    cel[4]=1
                else:
                   cel[4] = 0
               #3、获取模块的ID
                project_id_now = Project_info.objects.get(pname=cel[0],isdelete=0)
                model_id_now = Project_model.objects.get(modelname=cel[1],pnumber__pname=cel[0],isdelete=0)
                #获取接口信息
                is_distinct = Interface_info.objects.filter(interfacename=cel[2], url=cel[3], mnumber=model_id_now,
                                                            pnumber=project_id_now).values("id")

                # 判断接口是否存在
                if (is_distinct.exists()):
                    Interface_info.objects.filter(id=list(is_distinct)[0].get("id")).update(interfacename=cel[2], url=cel[3], type=cel[4], defaultpar=cel[5],
                                                                         remark=cel[6])

                else:
                    Interface_info.objects.create(interfacename=cel[2], url=cel[3], type=cel[4], defaultpar=cel[5],
                                                       remark=cel[6],
                                                       mnumber=model_id_now, pnumber=project_id_now, pname=cel[0], mname=cel[1])
        else:
            return HttpResponse(json.dumps(is_all_inter(table,row)))
    else:
        return HttpResponse(json.dumps({"code":-1,"msg":"请选择正确的模板"}))

    return HttpResponse(json.dumps({"code": 200, "msg": "导入成功"}))


"""
[上传用例模板]
作者：代代花
描述：用例集页面中的导入调取此接口，只有在模板头相同的情况下才允许导入
response：成功返回“OK”,失败返回“Fail”

"""
def upload_case(request):
    wb = xlrd.open_workbook(filename=None, file_contents=request.FILES['file'].read())  # 读取excel文件
    table = wb.sheets()[0]
    row = table.nrows  # 总行数
    #table_header =['项目名称', '用例集名称', '用例名称', '接口名称', '接口URL', '请求头', '入参','执行顺序']
    table_header = ['项目名称', '用例集名称', '用例名称', '接口名称', '接口URL', '请求头', '入参', '执行顺序', '检查点']
    # 判断模板是否正确，通过operator.eq() 比较两个list是否相等
    if(operator.eq(table_header,table.row_values(0))):
        #判断校验是否通过，如果不通过，返回错误信息
        if(is_all_case(table,row) == True):
            # print(is_all_case(table,row))
            for i in range(1, row):  # 获取每一行的数据
                cel = table.row_values(i)
                for c in range(len(cel)):
                    if(isinstance(cel[c],(str))):#如果是str去除空格
                        cel[c]=cel[c].replace(' ', '')#去除空格

                #1、获取模板的对象
                template_ids = Template_info.objects.get(pnumber__pname=cel[0], templatename=cel[1], isdelete=0)
                # 2、获取接口对象
                interface_id = Interface_info.objects.get(interfacename=cel[3], url=cel[4],pname=cel[0],isdelete=0)

                #判断用例是否存在

                is_case = Template_detail.objects.filter(templateid__pnumber__pname=cel[0],
                                                         templateid__templatename=cel[1],
                                                         usercaseid__usercasename=cel[2],
                                                         interfaceid__interfacename=cel[3], isdelete=0).values("usercaseid")
                if (is_case):
                    User_case.objects.filter(id=list(is_case)[0].get("usercaseid")).update(usercasename=cel[2], interfaceurl=cel[4], headerinfo=cel[5],
                                                    paraminfo=cel[6], isjoin=0, isheader=1, run_order=cel[7],
                                                    isequal=cel[8], status=0)

                else:
                    # 3、添加用例，返回用例对象
                    case = User_case.objects.create(usercasename=cel[2], interfaceurl=cel[4], headerinfo=cel[5],
                                                    paraminfo=cel[6], isjoin=0, isheader=1, run_order=cel[7],
                                                    isequal=cel[8],
                                                    interfaceid=interface_id, status=0)
                    # 4、添加接口明细表
                    Template_detail.objects.create(interfaceid=interface_id, templateid=template_ids,
                                                   usercaseid=case)

        else:
            return HttpResponse (json.dumps(is_all_case(table,row)))
    else:
        return HttpResponse(json.dumps({"code": -1, "msg": "请选择正确的模板"}))

    return HttpResponse(json.dumps({"code":200, "msg": "导入成功"}))


"""
[下载模板接口]
作者：代代花
描述：根据不同请求的地址，下载接口模板、用例模板，
/interface/down_inter_xls/，下载“接口导入模板.xlsx”
/interface/down_case_xls/，下载“用例导入模板.xlsx”
"""
def downloadTest(request):
    def file_iterator(file_name, chunk_size=512):#用于形成二进制数据
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    if(request.path =="/interface/down_inter_xls/"):
        the_file_name = "接口导入模板.xlsx" #导出文件的名
        response =StreamingHttpResponse(file_iterator(os.path.abspath("test.xlsx")))#这里创建返回
    elif(request.path =="/interface/down_case_xls/"):
        the_file_name = "用例导入模板.xlsx"  # 导出文件的名
        response = StreamingHttpResponse(file_iterator(os.path.abspath("test_case.xlsx")))  # 这里创建返回

    response['Content-Type'] = 'application/vnd.ms-excel'#注意格式
    response['Content-Disposition'] = "attachment;filename='{0}'".format(escape_uri_path(the_file_name))#注意filename 这个是下载后的名字
    return  response


"""
[校验导入的模板数据是否正确]
形参：table,row
返回值：只有校验通过的才提示True
"""
def is_all_case(table,row):
    for i in range(1, row):  # 获取每一行的数据
        cel = table.row_values(i)
        for c in range(len(cel)):
            if(isinstance(cel[c],(str))):
                cel[c] = cel[c].replace(' ', '')  # 去除空格
        is_pro = Project_info.objects.filter(pname=cel[0],isdelete=0)
        is_tep = Template_info.objects.filter(pnumber__pname=cel[0], templatename=cel[1], isdelete=0)
        # 判断项目名称和用例集是否存在
        if (is_pro.exists() and is_tep.exists()):

            # 判断接口是否存在
            is_inter = Interface_info.objects.filter(interfacename=cel[3], url=cel[4], isdelete=0)
            if (is_inter.exists()):
                # 判断用例是否存在
                # is_case = Template_detail.objects.filter(templateid__pnumber__pname=cel[0],
                #                                          templateid__templatename=cel[1],
                #                                          usercaseid__usercasename=cel[2],
                #                                          interfaceid__interfacename=cel[3], isdelete=0)
                # if (is_case):
                #     return ({"code": -1, "msg": "数据库中已存在，第%s行的例数据" % (i)})
                return True

            else:
                return ({"code": -1, "msg": "数据库中未匹配到,第%s行的接口名称和接口URL" % (i)})
        else:
            return ({"code": -1, "msg": "数据库中未匹配到,第%s行对应的项目和用例集" % (i)})
    return True


def is_all_inter(table,row):
    for i in range(1, row):  # 获取每一行的数据
        cel = table.row_values(i)
        for c in range(len(cel)):
            cel[c] = cel[c].replace(' ', '')  # 去除空格
        # 先查询导入的数据的项目名称和模块名称是否存在
        project_id = Project_info.objects.filter(pname=cel[0],isdelete=0)
        model_id = Project_model.objects.filter(modelname=cel[1], pnumber=project_id,isdelete=0)
        #判断项目和模块是否存在
        if (project_id.exists() and model_id.exists()):
            project_id_now = Project_info.objects.get(pname=cel[0],isdelete=0)
            # 3、获取模块的ID
            model_id_now = Project_model.objects.get(modelname=cel[1], pnumber=project_id,isdelete=0)
            is_distinct = Interface_info.objects.filter(interfacename=cel[2], url=cel[3], mnumber=model_id_now,
                                                        pnumber=project_id_now)
            # 判断接口是否存在
            # if (is_distinct.exists()):
            #     return ({"code": -1, "msg": "数据库中已存在，第%s行的数据" % (i)})
        else:
            return ({"code": -1, "msg": "数据库中未匹配到,第%s行对应的项目和模块！" % (i)})

    return True


"""
[根据项目，导出接口数据]
形参：table,row
返回值：只有校验通过的才提示True
"""
def export_interface(request):
    pro_name = request.GET.get("pro_name") #项目名称
    pro_mo_name = request.GET.get("pro_mo_name")#模块名称

    bk = xlrd.open_workbook(os.path.abspath("test.xlsx"))
    xlsc = copy(bk)  # 复制excel文件
    shtc = xlsc.get_sheet(0)  # 获取复制后的文件

    all_inter = list(Interface_info.objects.filter(pname=pro_name,mname=pro_mo_name,isdelete=0).\
        values("pname","mname","interfacename","url","type","defaultpar","remark"))
    for i in range(all_inter.__len__()):
        if (all_inter[i].get("type") == 1):
            type_inter = "POST"
        else:
            type_inter = "GET"
        shtc.write(i+1, 0, all_inter[i].get("pname"))
        shtc.write(i + 1, 1, all_inter[i].get("mname"))
        shtc.write(i + 1, 2, all_inter[i].get("interfacename"))
        shtc.write(i + 1, 3, all_inter[i].get("url"))
        shtc.write(i + 1, 4, type_inter)
        shtc.write(i + 1, 5, all_inter[i].get("defaultpar"))
        shtc.write(i + 1, 6, all_inter[i].get("remark"))

    the_file_name = "接口批量导出数据.xlsx"  # 导出文件的名
    save_file_name = "interface_all.xlsx"
    xlsc.save("interface_all.xlsx")

    def file_iterator(file_name, chunk_size=512):#用于形成二进制数据
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break


    response = StreamingHttpResponse(file_iterator(os.path.abspath(save_file_name)))  # 这里创建返回
    response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
    response['Content-Disposition'] = "attachment;filename='{0}'".format(
        escape_uri_path(the_file_name))  # 注意filename 这个是下载后的名字
    return response


"""
[导出用例集]
"""
def export_case(request):
    p_name = request.GET.get("pro_name")  # 项目名称
    template_name = request.GET.get("pro_mo_name")  # 用例集名称
    template_id = request.GET.get("pro_mo_id")#用例集ID
    usecase_name = request.GET.get("case_name")  # 用例名称
    # if(not usecase_name.strip()):
    #     usecase_name=None
    interfaece_name = request.GET.get("interface_name")  # 接口名称
    # if (not interfaece_name.strip()):
    #     interfaece_name = None
    bk = xlrd.open_workbook(os.path.abspath("test_case.xlsx"))
    xlsc = copy(bk)  # 复制excel文件
    shtc = xlsc.get_sheet(0)  # 获取复制后的文件

    list_usercase = list(Template_detail.objects.filter(Q(usercaseid__usercasename__contains=usecase_name) & Q(interfaceid__interfacename__contains=interfaece_name)).filter(templateid=template_id,isdelete=0).\
        values("usercaseid__usercasename","interfaceid__interfacename","usercaseid__interfaceurl","usercaseid__headerinfo",
               "usercaseid__paraminfo","usercaseid__run_order","usercaseid__isequal"))

    for i in range(list_usercase.__len__()):
        shtc.write(i+1, 0, p_name)
        shtc.write(i + 1, 1, template_name)
        shtc.write(i + 1, 2, list_usercase[i].get("usercaseid__usercasename"))
        shtc.write(i + 1, 3, list_usercase[i].get("interfaceid__interfacename"))
        shtc.write(i + 1, 4, list_usercase[i].get("usercaseid__interfaceurl"))
        shtc.write(i + 1, 5, list_usercase[i].get("usercaseid__headerinfo"))
        shtc.write(i + 1, 6, list_usercase[i].get("usercaseid__paraminfo"))
        shtc.write(i + 1, 7, list_usercase[i].get("usercaseid__run_order"))
        shtc.write(i + 1, 8, list_usercase[i].get("usercaseid__isequal"))

    the_file_name = "用例批量导出数据.xlsx"  # 导出文件的名
    the_save_name ="case_all.xlsx"
    xlsc.save(the_save_name)
    def file_iterator(file_name, chunk_size=512):#用于形成二进制数据
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break


    response = StreamingHttpResponse(file_iterator(os.path.abspath(the_save_name)))  # 这里创建返回
    response['Content-Type'] = 'application/vnd.ms-excel'  # 注意格式
    response['Content-Disposition'] = "attachment;filename='{0}'".format(
        escape_uri_path(the_file_name))  # 注意filename 这个是下载后的名字
    return response