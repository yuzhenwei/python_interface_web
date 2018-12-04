from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from DB.models  import *
import json


#用户登录
def login(request):

    if request.method =="POST":
        #查找不到账号则抛出异常
        try:
            username= request.POST.get("username",None) #获取用户名
            user_psw=User_info.objects.filter(username=username).values("password","name")[0]
        except IndexError:
            return HttpResponse(json.dumps({"msg":"-1"}))
        else:
            name = user_psw.get("name")
            if request.POST.get("pwd",None) == user_psw.get("password"):
                #用户名加入seesion，超时时间为6000S
                #生成随机字符串
                #写到用户浏览器cookies
                #保存到session中
                #在随机字符串对应的字典中设置相关内容
                request.session['username'] = name
                request.session['is_login'] = True
                request.session.set_expiry(6000)
                return HttpResponse(json.dumps({"msg":"1"}))
            else:
                return HttpResponse(json.dumps({"msg":"0"}))
    return render(request, "LoginPage/login.html")
def index(request):
  #session中获取值
  if request.session.get('is_login',None):
      return render(request,"LoginPage/index.html")
  else:
     return  redirect("LoginPage/login.html")


#返回首页
def  login_on(request):
    #判断session是否无效或过期，则返回登陆页
    username = request.session.get('username')
    if username is None:
        return redirect("/web/login")
    return render(request, "LoginPage/index.html")

#注销动作
def logout(request):
    username = request.session.get('username')
    if username!=None:
        del request.session['username']  #删除session
    return redirect("/web/login")

# 母版
def interface_base(request):
    username = request.session.get('username')
    if username is None:
        return redirect("/web/login")
    return render(request,"BasePage/interface_base.html")
