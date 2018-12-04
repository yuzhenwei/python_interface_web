# -*- coding: UTF-8 -*-
import requests
import json,time

METHODS = ['GET', 'POST']


class HttpRequest:
    def __init__(self, url, method, headers=None):
        """headers: 字典。 例：headers={'Content_Type':'text/html'}，cookies也是字典。"""
        self.url = url;
        self.method = method.upper()
        if self.method not in METHODS:
            raise ('不支持的method:{0}，请检查传入参数！'.format(self.method))
        self.set_headers(headers);

    def set_headers(self, headers):
        if headers:
            # 判断请求头的类型，如果不是dict,转换格式
            if not isinstance(headers, dict):
                headers = eval(headers)
        self.headers = headers

    def send(self, json_data=None, form_data=None, **kwargs):
        # 这里对时间进行参数化，指定%{=timne}%,把入参转化成字符串，并替换时间戳，再转成dict
        times = str(int(round(time.time() * 1000)))
        retime = "%{=time}%"
        data = ""
        if form_data != None:
            data = form_data
            if(not isinstance(form_data,(str))):
                form_data = json.dumps(form_data)

            if(retime in form_data ):
                form_data = form_data.replace(retime,times)
                form_data = json.loads(form_data)
            else:
                form_data = json.loads(form_data)


        if ( json_data != None):
            data = json_data
            if(not isinstance(json_data,(str))):
                json_data = json.dumps(json_data)

            if (retime in json_data):
                json_data = json_data.replace(retime, times)
                json_data = json.loads(json_data)
            else:
                json_data = json.loads(json_data)

        response = requests.request(method=self.method, headers=self.headers, url=self.url, json=json_data, data=form_data, **kwargs)
        response.encoding = 'utf-8'
        return response, self.url, self.headers, data
