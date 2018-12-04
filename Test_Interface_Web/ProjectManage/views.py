from django.shortcuts import render,redirect,HttpResponse
from DB import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

'''
项目首页,默认渲染出项目列表
'''
def search(request):
    project_names=models.Project_info.objects.filter(isdelete=0).values_list("pname", "pnumber")
    data={"project_names":project_names}
    if request.session.get('is_login', None):
        return render(request, 'ProjectPage/search_model.html', data)
    else:
        return redirect("/web/login")



'''
bootstrap-table分页
'''
def project_lists(request):
    offset = request.GET.get('offset')
    limit = request.GET.get('limit')
    pname = request.GET.get('pname')
    try:
        if(pname=='' or pname==None or pname=='--请选择--' or pname=='-1'):
            data_lists=models.Project_model.objects.filter(isdelete='0').values('pnumber__pname','pnumber',
                                                                  'modelname','mnumber','description').order_by('-mnumber')
        else:
            data_lists=models.Project_model.objects.filter(pnumber=pname,isdelete='0').values('pnumber__pname','pnumber',
                                                                  'modelname','mnumber','description').order_by('-mnumber')
        data_lists=list(data_lists)
        data = data_lists[int(offset):int(limit) + int(offset)]
        return HttpResponse(json.dumps({"retcode":0, "msg":"sucess","total":len(data_lists),"rows":data}))
    except:
        return HttpResponse(json.dumps({"retcode":-1, "msg":"查询出错！"}))


'''
新增模块
'''
def add_project(request):
    if request.method =='GET':
        return render(request,'ProjectPage/search_model.html')
    elif request.method =='POST':
        # 从前端获取字段值并写入数据库
        pnum = request.POST.get('Pn')
        mna = request.POST.get('modelname')
        des = request.POST.get('description')
        models.Project_model.objects.create(
            pnumber_id = pnum,
            modelname =  mna,
            description = des
        )
        return HttpResponse('模块新增成功啦！')



'''
编辑项目
'''
def edit_project(request):
        pnum = request.POST.get('editPn')
        mna = request.POST.get('modelnames')
        mnum = request.POST.get('mnumbers')
        des = request.POST.get('descriptions')
        # print(pnum,mna,mnum,des)
        models.Project_model.objects.filter(mnumber= mnum).update(pnumber=pnum,modelname=mna,description=des)
        return HttpResponse('项目编辑成功啦！')

'''
删除项目
'''
def delete_project(request):
    if request.method=='GET':
        return render(request,'ProjectPage/search_model.html')
    elif request.method=='POST':
        mnum = request.POST.get('mnu')
        data = models.Interface_info.objects.filter(mnumber_id=mnum)
        if data:
            return HttpResponse('该模块下含有接口数据，暂时不能删除啦！')
        else:
            models.Project_model.objects.filter(mnumber =mnum).update(isdelete='1')
            return HttpResponse('该模块已经删除成功啦！')

