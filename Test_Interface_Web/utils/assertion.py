#-*- coding: UTF-8 -*-
import json
from utils.mail import Email

class Jsonprint():

    def __init__(self):
        self.resulttype=1   #检查点状态 1为通过，2为不通过

    '''
    #递归查找value值
    def print_json_key(self,input_json,key,type=1):
        key_value=''
        if isinstance(input_json,dict):
            for json_result in input_json.values():
                if key in input_json.keys():
                    key_value = input_json.get(key)
                else:
                    self.print_json_key(json_result,key)
        elif isinstance(input_json,list):
            for json_array in input_json:
                self.print_json_key(json_array,key)
        if key_value!='':
            self.key_info.append(key_value)
    '''



    '''
    #根据检查点计算结果，type1代表是否等于,2代表不等于,3代表包含,4代表不包含
    def getcheckcount(self,resultinfo,checkinfo,type):
        check_info=[]     #保存检查点
        check_str=''     #检查点内容
        #判断是否为空
        i=len(checkinfo)
        if type==1:
            if(i>0):
                for j in range(i):
                    for key,value in checkinfo[j].items():
                        self.print_json_key(resultinfo,key)
                        if value in self.key_info:
#                            check_str='<tr><td>'+key+':'+value+'</td><td><span class="glyphicon glyphicon-ok" style="color: rgb(0, 167, 0);"></span></td></tr>'
#                            check_info.append(check_str)
                            self.okcount+=1
                        else:
#                            check_str='<tr><td>'+key+':'+value+'</td><td><span class="glyphicon glyphicon-remove" style="color: rgb(255, 0, 0);"></span></td></tr>'
#                            check_info.append(check_str)
                            self.failcount+=1
                        self.key_info.clear()
        elif type==2:
                for j in range(i):
                    for key,value in checkinfo[j].items():
                        self.print_json_key(resultinfo,key)
                        if value not in self.key_info:
                            check_str='<tr><td>'+key+':'+value+'</td><td><span class="glyphicon glyphicon-ok" style="color: rgb(0, 167, 0);"></span></td></tr>'
                            check_info.append(check_str)
                            self.okcount+=1
                        else:
                            check_str='<tr><td>'+key+':'+value+'</td><td><span class="glyphicon glyphicon-remove" style="color: rgb(255, 0, 0);"></span></td></tr>'
                            check_info.append(check_str)
                            self.failcount+=1
                        self.key_info.clear()
        return check_info
        '''


    #等于与不等于断言,type为1检验等于，2校验不等于
    def checkresult(self,json_info,checkinfo,type):
        #print(str(json_info).encode('utf-8'))
        check_info=[]   #检查点内容

        #格式化去除空格和转换""
        json_info=str(json_info).replace("\\", "")
        json_info=json_info.replace('"', "")
        json_info=json_info.replace("'", "")
        json_info3=json_info.replace(' ','')

        #检查点
        c_info=checkinfo.split(';')
        for i in range(0,len(c_info)):
            if type==1:
                if(json_info3.find(c_info[i])==-1):
                    check_str='<tr><td>'+c_info[i]+'</td><td>等于</td><td><span class="glyphicon glyphicon-remove" style="color: rgb(255, 0, 0);"></span></td></tr>'
                    check_info.append(check_str)
                    self.resulttype=2
                else:
                    check_str='<tr><td>'+c_info[i]+'</td><td>等于</td><td><span class="glyphicon glyphicon-ok" style="color: rgb(0, 167, 0);"></span></td></tr>'
                    check_info.append(check_str)


            elif type==2:
                if(json_info3.find(c_info[i])==-1):
                    check_str='<tr><td>'+c_info[i]+'</td><td>不等于</td><td><span class="glyphicon glyphicon-ok" style="color: rgb(0, 167, 0);"></span></td></tr>'
                    check_info.append(check_str)

                else:
                    check_str='<tr><td>'+c_info[i]+'</td><td>不等于</td><td><span class="glyphicon glyphicon-remove" style="color: rgb(255, 0, 0);"></span></td></tr>'
                    check_info.append(check_str)
                    self.resulttype=2
        #print(check_info)
        return  check_info

    # 将实际请求结果展示在页面
    def show_real_data(self, url, headers, real_data):
        data = "<tr><td width='10%' >" + str(url) \
               + "</td><td width='30%' >" + str(headers) \
               + "</td><td width='30%' >" + str(real_data) + "</td></tr>"
        return data


if __name__=="__main__":
    str_info={"msg": "{\"code\":0,\"msg\":\"\u6210\u529f\",\"data\":[{\"recomId\":1119215,\"recordId\":null,\'changedRemarkName\':false,\"eSignSerial\":[\"05c5b4a0e7674326a5fce2cc0fa1531b\"]}]}", "resulttype": 200}

    '''
    jp=Jsonprint()
    print(jp.getcheckcount(resultinfo=str,checkinfo=[{"changedRemarkName":False}],type=1))
    print(jp.okcount)
    print(jp.failcount)
    '''

    '''
    e = Email(title='自动化测试报告',
              message="""这是本次测试报告链接:http://10.9.2.142/report/testreport?id=12""",
              receiver='shilongzi@7lk.com;daidaihua@7lk.com;zijing@7lk.com;shasha@7lk.com',
              server='smtp.126.com',
              sender='qlktest@126.com',
              password='qlk123456',
              path=''
              )
    e.send()
    '''

