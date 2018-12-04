"""
添加用于接口测试的client，对于HTTP接口添加HTTPClient，发送http请求。
还可以封装TCPClient，用来进行tcp链接，测试socket接口等等。
"""

import requests
import socket
import json
import time

METHODS = ['GET', 'POST', 'HEAD', 'TRACE', 'PUT', 'DELETE', 'OPTIONS', 'CONNECT']


class UnSupportMethodException(Exception):
    """当传入的method的参数不是支持的类型时抛出此异常。"""
    pass


class HTTPClient(object):
    """
    http请求的client。初始化时传入url、method等，可以添加headers和cookies，但没有auth、proxy。

    >>> HTTPClient('http://www.baidu.com').send()
    <Response [200]>

    """
    def __init__(self, url, method='GET', headers=None, cookies=None):
        """headers: 字典。 例：headers={'Content_Type':'text/html'}，cookies也是字典。"""
        self.url = url
        self.session = requests.session()
        self.method = method.upper()
        if self.method not in METHODS:
            raise UnSupportMethodException('不支持的method:{0}，请检查传入参数！'.format(self.method))

        self.set_headers(headers)
        self.set_cookies(cookies)

    def set_headers(self, headers):
        if headers:
            # 判断请求头的类型，如果不是dict,转换格式
            if(not isinstance(headers,(dict))):
                headers = eval(headers)
            self.session.headers.update(headers)

    def set_cookies(self, cookies):
        if cookies:
            self.session.cookies.update(cookies)

    def send(self, params=None, data=None, **kwargs):
        # 这里对时间进行参数化，指定%{=timne}%,把入参转化成字符串，并替换时间戳，再转成dict
        times = str(int(round(time.time() * 1000)))
        #print(times,params,data)
        return_data = ""

        retime ="%{=time}%"
        if( data != None):
            data = json.dumps(data)
            #print(data)
            if(retime in data ):
                data = data.replace(retime,times)
                data = json.loads(data)
                #print(data,type(data))
            return_data = data
        if ( params != None):
            params = json.dumps(params)
            if (retime in params):
                params = params.replace(retime, times)
                params = json.loads(params)
                #rint(params)
            return_data = params
        response = self.session.request(method=self.method, url=self.url, json=params, data=data, **kwargs)
        response.encoding = 'utf-8'
        #print(response.text)
        return response, self.url, self.session.headers, return_data


class TCPClient(object):
    """用于测试TCP协议的socket请求，对于WebSocket，socket.io需要另外的封装"""
    def __init__(self, domain, port, timeout=30, max_receive=102400):
        self.domain = domain
        self.port = port
        self.connected = 0  # 连接后置为1
        self.max_receive = max_receive
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(timeout)

    def connect(self):
        """连接指定IP、端口"""
        if not self.connected:
            try:
                self._sock.connect((self.domain, self.port))
            except socket.error as e:
                print(e)
            else:
                self.connected = 1

    def send(self, data, dtype='str', suffix=''):
        """向服务器端发送send_string，并返回信息，若报错，则返回None"""
        if dtype == 'json':
            send_string = json.dumps(data) + suffix
        else:
            send_string = data + suffix
        self.connect()
        if self.connected:
            try:
                self._sock.send(send_string.encode())
            except socket.error as e:
                print(e)

            try:
                rec = self._sock.recv(self.max_receive).decode()
                if suffix:
                    rec = rec[:-len(suffix)]
                return rec
            except socket.error as e:
                print(e)

    def close(self):
        """关闭连接"""
        if self.connected:
            self._sock.close()
