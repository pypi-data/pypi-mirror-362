import requests
import json as json_module

class Response:
    """响应类，封装requests响应对象"""
    
    def __init__(self, response):
        self._response = response
        self._content = None
        
    @property
    def headers(self):
        """返回响应头"""
        return dict(self._response.headers)
    
    @property
    def status_code(self):
        """返回响应状态码"""
        return self._response.status_code
    
    def close(self):
        """关闭连接并释放资源"""
        self._response.close()
    
    @property
    def content(self):
        """以字节形式返回响应内容"""
        if self._content is None:
            self._content = self._response.content
        return self._content
    
    @property
    def text(self):
        """以字符串形式返回响应内容"""
        return self._response.text
    
    def json(self):
        """以字典形式返回响应内容"""
        return self._response.json()

def request(method, url, data=None, json=None, headers={}):
    """发送网络请求"""
    try:
        response = requests.request(
            method=method,
            url=url,
            data=data,
            json=json,
            headers=headers
        )
        return Response(response)
    except Exception as e:
        print(f"请求失败: {e}")
        raise

def head(url, **kw):
    """发送HEAD请求"""
    return request("HEAD", url, **kw)

def get(url, **kw):
    """发送GET请求"""
    return request("GET", url, **kw)

def post(url, **kw):
    """发送POST请求"""
    return request("POST", url, **kw)

def put(url, **kw):
    """发送PUT请求"""
    return request("PUT", url, **kw)

def patch(url, **kw):
    """发送PATCH请求"""
    return request("PATCH", url, **kw)

def delete(url, **kw):
    """发送DELETE请求"""
    return request("DELETE", url, **kw)
