from django.http.response import HttpResponse
import json,logging
from utils.HttpClass import HttpRequest
from utils.joinjson import JoinPar
from DB.models import *


header_form = "application/x-www-form-urlencoded"
header_json = "application/json"
null=''
true = "'True'"
false = "'False'"
logger = logging.getLogger("sourceDns.webdns.views")

"""
【执行测试用例】
    形参：用例的ID
    res:接口返回值
"""
def run_case(caseid,pubpar):
    caseinfo = case_info(caseid) #查询数据库获取接口信息
    if(pubpar!=None and pubpar!=""):
        case_url_url = caseinfo.get("interfaceurl")#获取接口url
        case_url = re_url_par(pubpar,case_url_url)
        # print("替换后的URL:",case_url)
        case_paraminfo_info = caseinfo.get("paraminfo")#获取入参
        case_paraminfo = re_url_par(pubpar, case_paraminfo_info)
        # print("替换后的入参:",case_paraminfo)
        # logger.info("替换后的入参:" + case_paraminfo)
    else:
        case_url = caseinfo.get("interfaceurl")  # 获取接口url
        case_paraminfo = caseinfo.get("paraminfo")  # 获取入参

    case_isjoin = caseinfo.get("isjoin")#是否关联，1为关联
    case_method = caseinfo.get("interfaceid__type")#获取请求方式
    rejoin_key = caseinfo.get("rejoin_key") #获取被依赖的key
    if (rejoin_key != None and rejoin_key != "" and rejoin_key != []):
        rejoin_key =rejoin_key.split(",")
    if case_method == 1:
        case_method = "POST"
    else:
        case_method = "GET"
    headerinfo = caseinfo.get("headerinfo").replace(' ','') #获取请求头
    join_values=None
    actual_url = ""
    actual_headers = ""
    actual_data = ""
    #4、判断是否含有关联
    if(case_isjoin == 1):
        joininfo = caseinfo.get("joininfo")  # 获取关联详情
        join_values = join_case_value(joininfo)#执行关联用例
        #print("____",join_values)
    # 6、拼接数据，执行用例
        rel_paraminfo =  re_paraminfo(case_paraminfo,joininfo,join_values)
        if (header_json in headerinfo):
            logger.info("执行用例:" + case_url+case_method+str(headerinfo)+str(rel_paraminfo))
            res, actual_url, actual_headers, actual_data = HttpRequest(url=case_url, method=case_method, headers=headerinfo).send(json_data=rel_paraminfo)
        else:
            logger.info("执行用例:" + case_url + case_method + str(headerinfo)+str(rel_paraminfo))
            res, actual_url, actual_headers, actual_data = HttpRequest(url=case_url, method=case_method, headers=headerinfo).send(form_data=rel_paraminfo)
    else:
        if(case_method =="GET"):
            case_url =case_url+"?"+case_paraminfo
            logger.info("执行用例:" + case_url + case_method + str(headerinfo))
            res, actual_url, actual_headers, actual_data = HttpRequest(url=case_url, method=case_method,headers=headerinfo).send()
        else:
            if(header_json in headerinfo):
                logger.info("执行用例:" + case_url + case_method + str(headerinfo)+str(case_paraminfo))
                res, actual_url, actual_headers, actual_data = HttpRequest(url=case_url, method=case_method, headers=headerinfo).send(json_data=case_paraminfo)
            else:
                logger.info("执行用例:" + case_url + case_method + str(headerinfo)+str(case_paraminfo))
                res, actual_url, actual_headers, actual_data = HttpRequest(url=case_url, method=case_method, headers=headerinfo).send(form_data=case_paraminfo)

    #获取被关联的值,更新数据库
    if(rejoin_key == None or rejoin_key == "" or rejoin_key == []):
        User_case.objects.filter(id=caseid).update(status=1)
    else:
        rejoin_keys = updata_status(res.text,rejoin_key)
        User_case.objects.filter(id=caseid).update(status=1, rejoin_value=rejoin_keys)
    resulttype = res.status_code
    return json.dumps({
        "msg": res.text,
        "resulttype": resulttype,
        "actual_url": actual_url,
        "actual_headers": actual_headers,
        "actual_data": actual_data})




"""
【查询用例】
    根据用例ID查询用例
    形参：用例ID
    res:返回用例详情，类型dict
"""
def case_info(caseid):
    case_list = list(
        User_case.objects.filter(id=caseid).values("interfaceurl", "isheader", "headerinfo", "paraminfo", "isjoin",
                                                   "joininfo", "interfaceid__type","rejoin_key"))
    return case_list[0]



"""
【执行关联用例】
    形参：joininfo（依赖的关联内容）
    res:被依赖接口的{key:value}
"""
def join_case_value(joininfo):
    # 5、获取关联字段获取关
    joininfo = eval(joininfo)
    for join_case in joininfo:
        join_case_id = join_case.get("caseid")  # 获取关联的用例ID
        #根据用例查接口详情
        caseinfo = case_info(join_case_id)
        isjoin = caseinfo.get("isjoin")
        #rejoin_key_list = caseinfo.get("rejoin_key").split(",") #获取被依赖的key
        #判断是否关联递归查询
        if(isjoin ==3):
            joininfo_l = caseinfo.get("joininfo")
            join_case_value(joininfo_l)
        else:
            # 判断依赖的用例执行状态和被依赖的值是否正确
            rejoin_status = list(User_case.objects.filter(id=join_case_id).values("status", "rejoin_key","rejoin_value"))
            status = rejoin_status[0]["status"]
            rejion_keys_list = rejoin_status[0]["rejoin_key"].split(",") #获取被依赖的key
            rejoin_values = rejoin_status[0]["rejoin_value"]
            # 如果初始化状态，执行依赖用例
            # 如果是已执行状态,直接取返回值
            if (status == 0):
                case = case_info(join_case_id)
                case_method = case.get("interfaceid__type")  # 获取请求方式
                if case_method == 1:
                    case_method = "POST"
                else:
                    case_method = "GET"
                if (header_json in case.get("headerinfo").replace(' ','')):
                    res, _, _, _ = HttpRequest(method=case_method,url=case.get("interfaceurl"),headers=case.get("headerinfo").replace(' ','')).\
                        send(json_data=case.get("paraminfo"));
                else:
                    res, _, _, _ = HttpRequest(method=case_method, url=case.get("interfaceurl"), headers=case.get("headerinfo").replace(' ','')). \
                        send(form_data=case.get("paraminfo"));

                #更新数据数据库的状态和值
                if (rejion_keys_list == None or rejion_keys_list == "" or rejion_keys_list ==[]):
                    User_case.objects.filter(id=join_case_id).update(status=1)
                else:
                    rejoin_keys = updata_status(res.text, rejion_keys_list)
                    User_case.objects.filter(id=join_case_id).update(status=1, rejoin_value=rejoin_keys)
                    #print("111",rejoin_keys)
                return eval(rejoin_keys)
            else:
                rejoin_values = eval(rejoin_values)#转换为字典类型
                #print("222", rejoin_values)
                return rejoin_values

"""
【替换接口请求参数】
    形参：接口参数，关联详情，关联的值
    res:替换后的接口参数，
"""
def re_paraminfo(case_paraminfo,joininfo,join_values):
    re_paraminfo=None
    join_info = eval(joininfo)
    for j in range(len(join_info)):
        jsonpar = join_info[j]["jsonpar"].split(',')
    for jpar in jsonpar:
        qw = jpar.split("=")
        in_key = qw[0]  # 入参中的key
        out_key = qw[1]  # 需要依赖的key
        out_value = join_values.get(out_key)  # 获取出参的值
        jp=JoinPar()
        #print("qq",eval(case_paraminfo),in_key,out_value)
        #re_paraminfo = jp.key_replace_value(eval(case_paraminfo),in_key,out_value)  # 关联接口替换
        re_paraminfo = (jp.str_replace(case_paraminfo,in_key,out_value))
        case_paraminfo = re_paraminfo
        #print("aa",re_paraminfo)
    return json.loads(case_paraminfo);


"""
【response中获取被依赖的值】
    形参：response,rejion_keys（被依赖的值）
    res:返回str类型的{key:value}依赖值
"""
def updata_status(res,rejion_keys):
    jp = JoinPar()  # 创建一个对象，获取key,value
    for keys in rejion_keys:
        jp.print_json_key(eval(res), keys)
        rejoin_values = json.dumps(jp.key_info)
    return rejoin_values;


"""
【初始化用例集】
    形参：模板ID
    res:0：未执行，1：已执行
    描述：更新用例集的执行状态为0（0：未执行，1：已执行）,清空被依赖的字段
    """
def start_ini_templet(request):
    templetids = request.GET.get("templetid", 0)
    #1、查询用例集
    case_list = list(Template_detail.objects.filter(templateid=templetids,usercaseid__gte=0).values("usercaseid"));
    #2、初始化用例为，0未执行，清空对外提供的依赖值
    sum_count = 0 #初始化更新的总数
    for case in case_list:
        id = case.get("usercaseid")
        counts = User_case.objects.filter(id=id).update(status=0,rejoin_value="")
        sum_count = sum_count+counts
    #print("初始化:",templetids)
    if(sum_count == case_list.__len__() ):
        return HttpResponse(json.dumps({"msg": "初始化用例集完成"}))
    else:
        return HttpResponse(json.dumps({"msg": "初始化用例集失败"}))

"""
【执行用例入口】
    形参：request
    res:接口的response结果
"""
# def start_run_case(request):
#     caseid = request.POST.get("caseid", 0)
#     # 3、获取用例详情
#     res_text = run_case(caseid,)
#     return HttpResponse(res_text)

"""
【公共参数替换】
    形参：pubpar（公共参数）,str_val（替换的url或者入参）
    res:返回string类型的值
"""
def re_url_par(pubpar,str_val):
    keys = list(pubpar.keys())
    # print(keys)
    for i in keys:
        str = "{%s}" % i
        # print(str, pubpar.get(i))
        if (str in str_val):
            str_val = str_val.replace(str, pubpar.get(i))
    return str_val
