# -*- coding:utf-8 -*-

from typing import Optional, Dict, Any
import requests
import hashlib
import time
import os


class BaseApi:

    def __init__(self, server: str, port: int,
                 apikey: str, apisecret: str,
                 use_ssl: Optional[bool] = False) -> None:
        """初始化

        初始化接口

        :param str server: 服务器地址
        :param int port: 服务器web端口
        :param str apikey: OpenApi key
        :param str apisecret: _OpenApi secret
        :param bool use_ssl: 是否使用HTTPS, defaults to False
        """
        self.sessid: str = ''
        self.url: str = ''
        self.server: str = server
        self.port: int = port
        self.use_ssl: bool = use_ssl
        self.apikey: str = apikey
        self.apisecret: str = apisecret
        self.params: Dict[str, Any] = {}

    def sign_para(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """请求参数签名

        字典参数排序，计算sign，返回对应的新字典参数
        :param params:
        :return: 返回带sign的新字典参数
        """

        sort_params = sorted(params.items(), key=lambda t: t[0], reverse=False, )
        # {'b':2,'a':1,'c':3} -> [('a', 1), ('b', 2), ('c', 3)]

        urlstr = self.apisecret
        for item in sort_params:
            for x in item:
                urlstr += str(x)
        urlstr += self.apisecret
        sign = hashlib.md5(urlstr.encode('utf-8')).hexdigest()

        params.update({"sign": sign})

        self.params = {}
        self.params = params

        return params

    # http request get json data ,return dict
    def request(self, method_params: Dict[str, Any], http_method: str = 'post') -> Dict[str, Any]:
        """ http/https请求

        Winmail 6.6的上传附件接口处理，sign中不计算attachfile
        :param method_params: OpenAPI请求参数字典
        :param http_method: HTTP请求类型 get/post
        :return:
        """

        if 'attachfile' in method_params:
            attch_file = method_params['attachfile']
            if isinstance(attch_file, list):
                files = []
                for f in attch_file:
                    fname = os.path.split(f)[1]
                    files.append(('attachfile[]', (fname, open(f, 'rb'))))
            else:
                files = {'attachfile': open(attch_file, 'rb')}

            method_params.pop('attachfile')

            try:
                response = requests.post(self.url, self.sign_para(method_params), files=files, verify=False)
            except Exception as e:
                return {'result': 'error', 'info': 'http connect error 0 : %s' % e}
        else:

            try:
                if http_method == "get":
                    response = requests.get(self.url, self.sign_para(method_params), verify=False)
                else:
                    response = requests.post(self.url, self.sign_para(method_params), verify=False)
            except Exception as e:
                return {'result': 'error', 'info': 'http connect error 1 : %s' % e}

        if response.status_code == 200:
            # Winmail 本身newmsg.reset接口没有返回json数据，执行后就完成。单独处理下
            # (6.6 0812版本已经加入json返回结果, 注释掉)
            # if method_params['method'] == 'newmsg.reset':
            #    return {"result": 'ok'}
            try:
                data = response.json()
            except Exception as e:
                return {'result': 'error', 'info': '%s : %s' % (method_params['method'], e)}
        else:
            data = {"result": "error", 'info': "http status %s." % response.status_code}

        return data

    # login 
    def login(self, user: str, pwd: str, manage_path: Optional[str] = '', tid: Optional[int] = 0) -> Dict[str, Any]:
        """认证

        登陆成功将把sessid赋值给实例的sessid。
        返回结果为API接口返回的JSON字符串转换的dict。

        :param str user: 用户名
        :param str pwd: 密码
        :param str manage_path: 管理端路径默认是admin，6.6版本的Winmail可以在管理工具后台修改管理端路径。
                如果值为空是邮箱用户。
        :param int tid: Webmail的themes，tid=6时为手机web界面
        :return: dict {result: ok/error, info: ""}
        """

        # HTTPS选择
        if self.use_ssl:
            url_scheme = 'https://'
        else:
            url_scheme = 'http://'

        if manage_path:
            self.url = url_scheme + self.server + ':' + str(self.port) + '/' + manage_path + '/openapi.php'
        else:
            self.url = url_scheme + self.server + ':' + str(self.port) + '/openapi.php'

        # method=login
        timestamp = str(int(time.time()))
        param_dict = {'user': user, 'pass': pwd}
        param_dict.update({"apikey": self.apikey, "method": "login", "timestamp": timestamp})

        if not manage_path:
            param_dict.update({'tid': str(tid)})

        result = self.request(param_dict)
        if result['result'] == 'ok':
            self.sessid = result['info']['sessid']
        return result

    # update session id
    def update_session(self) -> bool:
        """ 更新Sessid

        :return: True/False
        """
        if not self.sessid:
            return False
        timestamp = str(int(time.time()))
        param_dict = {"apikey": self.apikey, "method": "updatesession", "sessid": self.sessid, "timestamp": timestamp}
        result = self.request(param_dict)

        if result['result'] == 'ok':
            return True
        return False

    # method function return dict data
    def do_api(self, http_method: str = 'post', **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """接口请求

        执行OpenAPI请求，并返回rquests执行结果。

        :param dict kwargs: OpenApi方法和参数集合的字典 {'method': 'user', 'domain': 'winmail.cn' .....}
        :param http_method: HTTP请求类型 get/post

        :return: Dict {result: ok/error, info: ""}
        """

        param_dict: Dict[str, Any] = kwargs

        if not self.url or not self.sessid:

            self_name = self.__class__.__name__

            for name, obj in globals().items():
                if obj is self:
                    self_name = repr(name)

            return {"result": "error",
                    "info": "Use login first %s.login(user, pwd, manage_path) " % self_name}

        timestamp = str(int(time.time()))

        if 'sessid' not in param_dict:
            param_dict.update({'sessid': self.sessid})
        if 'apikey' not in param_dict:
            param_dict.update({"apikey": self.apikey})
        if 'timestamp' not in param_dict:
            param_dict.update({"timestamp": timestamp})
        result = self.request(param_dict, http_method=http_method)

        return result

    def post_api(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """接口请求

        执行OpenAPI的POST请求，并返回rquests执行结果。

        :param dict kwargs: OpenApi方法和参数集合的字典 {'method': 'user', 'domain': 'winmail.cn' .....}

        :return: Dict {result: ok/error, info: ""}
        """

        return self.do_api('post', **kwargs)

    def get_api(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """接口请求

        执行OpenAPI的GET请求，并返回rquests执行结果。

        :param dict kwargs: OpenApi方法和参数集合的字典 {'method': 'user', 'domain': 'winmail.cn' .....}

        :return: Dict {result: ok/error, info: ""}
        """

        return self.do_api('get', **kwargs)

    def logout(self) -> Dict[str, Any]:
        """ 退出登陆

        退出接口登陆，清空服务器的sessid

        :return: Dict
        """

        timestamp = str(int(time.time()))
        param_dict = {"apikey": self.apikey, "method": "logout", "sessid": self.sessid, "timestamp": timestamp}
        result = self.request(param_dict)

        return result
