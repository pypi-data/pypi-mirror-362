# -*- coding:utf-8 -*-
from typing import Optional, Literal, Dict, Any

from .Base import BaseApi
from .resources.user import *
from .resources.admin import *


class OpenApi:
    """
    api = OpenApi(server, port, apikey, apisecret, use_ssl=False)

    # admin login
    login_result = api.login('adminUser', 'myPassword', manage_path='admin')

    method_params = {
        "method": "user",
        "domain": "test.com"
    }

    method_result = api.get_api(**method_params)


    # user login pc: tid=0, mobile: tid=6
    login_result = api.login('adminUser', 'myPassword', tid=0)

    method_params = {
        "method": "msglist",
    }

    method_result = api.get_api(**method_params)
    """

    def __init__(
            self,
            server: str,
            port: int,
            apikey: str,
            apisecret: str,
            use_ssl: Optional[bool] = False,
    ) -> None:
        """
        初始化OpenApi接口

        :param server: 服务器地址
        :param port:  端口
        :param apikey: APIkey
        :param apisecret: API密钥
        :param use_ssl:  是否使用SSL端口
        :return: None
        """
        self._openapi = BaseApi(
            server=server,
            port=port,
            apikey=apikey,
            apisecret=apisecret,
            use_ssl=use_ssl,
        )

        # admin 接口
        self._domain: Optional[Domain] = None
        self._domainalias: Optional[DomainAlias] = None
        self._user: Optional[User] = None
        self._useralias: Optional[UserAlias] = None
        self._group: Optional[Group] = None
        self._adminuser: Optional[AdminUser] = None
        # user接口
        self._msglist: Optional[MsgList] = None
        self._folders: Optional[Folders] = None
        self._addressbook: Optional[AddressBook] = None
        self._msgnum: Optional[MsgNum] = None
        self._upload: Optional[Upload] = None
        self._newmsg: Optional[NewMsg] = None
        self._readmsg: Optional[ReadMsg] = None
        self._netaddressbook: Optional[NetaddressBook] = None
        self._systemgroup: Optional[SystemGroup] = None

        self._is_login: Literal["", "user", "admin"] = ''  # 标记是否登陆: ''/‘user’/'admin' 未登陆、用户、管理员

        self._openapi = BaseApi(server=server, port=port,
                                apikey=apikey, apisecret=apisecret,
                                use_ssl=use_ssl)

    def _check_login(self, login_type: Literal["", "user", "admin"]) -> None:
        """检查认证"""
        if not self._is_login:
            raise PermissionError("Please call `login()` first!")
        elif self._is_login != login_type:
            raise AttributeError(f"Winmail {self._is_login} api does not support this method.")

    @property
    def adminuser(self) -> AdminUser:
        """获取 AdminUser 实例（仅在 admin 模式下可用）"""
        self._check_login('admin')
        return self._adminuser

    @property
    def domain(self) -> Domain:
        """获取 Domain 实例（仅在 admin 模式下可用）"""
        self._check_login('admin')
        return self._domain

    @property
    def domainalias(self) -> DomainAlias:
        """获取 DomainAlias 实例（仅在 admin 模式下可用）"""
        self._check_login('admin')
        return self._domainalias

    @property
    def useralias(self) -> UserAlias:
        """获取 UserAlias 实例（公在 admin 模式下可用）"""
        self._check_login('admin')
        return self._useralias

    @property
    def user(self) -> User:
        """获取 User 实例（仅在 admin 模式下可用）"""
        self._check_login('admin')
        return self._user

    @property
    def group(self) -> Group:
        """获取 Group 实例（仅在 admin 模式下可用）"""
        self._check_login('admin')
        return self._group

    @property
    def msglist(self) -> MsgList:
        """获取 Msglist 实例（仅在 user 模式下可用）"""
        self._check_login('user')
        return self._msglist

    @property
    def readmsg(self) -> ReadMsg:
        """获取 ReadMsg 实例（仅在 user 模式下可用"""
        self._check_login('user')
        return self._readmsg

    @property
    def msgnum(self) -> MsgNum:
        """获取 MsgNum 实例（仅在 user 模式下可用）"""
        self._check_login('user')
        return self._msgnum

    @property
    def newmsg(self) -> NewMsg:
        """获取 NewMsg 实例（仅在 user 模式下可用）"""
        self._check_login('user')
        return self._newmsg

    @property
    def upload(self) -> Upload:
        """获取 Upload 实例（仅在 user 模式下可用）"""
        self._check_login('user')
        return self._upload

    @property
    def folders(self) -> Folders:
        """获取 Folders 实例（仅在 user 模式下可用）"""
        self._check_login("user")
        return self._folders

    @property
    def addressbook(self) -> AddressBook:
        """获取 AddressBook 实例（仅在 user 模式下可用）"""
        self._check_login("user")
        return self._addressbook

    @property
    def netaddressbook(self) -> NetaddressBook:
        """获取 NetaddressBook 实例（仅在 user 模式下可用）"""
        self._check_login('user')
        return self._netaddressbook

    @property
    def systemgroup(self) -> SystemGroup:
        """获取 SystemGroup 实例（仅在 user 模式下可用）"""
        self._check_login('user')
        return self._systemgroup

    @property
    def sessid(self):
        """获取 sessid """
        return self._openapi.sessid

    def login(
            self,
            user: str,
            pwd: str,
            manage_path: str = "",
            tid: int = 0,
    ) -> Dict[str, Any]:
        """ 登陆认证

        登陆并修改登陆状态。

        :param user: 认证邮箱用户名
        :param pwd:  密码
        :param manage_path: 调用管理端接口请写入管理地址，用户端调用请忽略，【winmail管理工具中系统设置-高级设置-系统参数-HTTP配置中查看】
        :param tid: 用户端调用参数，手机风格6，否则默认为0。参考web代码中用户登陆风格。
        :return: Dict
            管理端返回：
            {
                "result": "ok",
                "info":
                {
                    “ sessid ”:  "efd24f9f63d69d6f6f169b235822ca5875eb2bae",
                    “ user ”:  "admin"
                }
            }
            用户端返回：
            {
            "result": "ok",
            "info":
                {
                “ sessid ”:  "1a2db1b0edda735295508723d8c6a962",
                “uid”: "test",
                “email”: " test@test.com ",
                “fullname”: "测试用户",
                “mobile”: "13900000000",
                “company”: "华兆科技",
                “department”: "系统研发部",
                “jobtitle”: "工程帅",
                “office”: "",
                “officephone”: "",
                “homeaddress”: "",
                “homephone”: "",
                }
            }
        """

        # 先登录
        login_result = self._openapi.login(
            user=user,
            pwd=pwd,
            manage_path=manage_path,
            tid=tid,
        )

        if login_result["result"].lower() == "ok":
            if manage_path:
                self._is_login = 'admin'

                self._user = User(self._openapi)
                self._useralias = UserAlias(self._openapi)
                self._group = Group(self._openapi)
                self._adminuser = AdminUser(self._openapi)
                self._domain = Domain(self._openapi)
                self._domainalias = DomainAlias(self._openapi)

            else:
                self._is_login = 'user'

                self._msglist = MsgList(self._openapi)
                self._folders = Folders(self._openapi)
                self._addressbook = AddressBook(self._openapi)
                self._msgnum = MsgNum(self._openapi)
                self._readmsg = ReadMsg(self._openapi)
                self._upload = Upload(self._openapi)
                self._newmsg = NewMsg(self._openapi)
                self._netaddressbook = NetaddressBook(self._openapi)
                self._systemgroup = SystemGroup(self._openapi)

        return login_result

    def updatesession(self) -> bool:
        """更新会话

        更新Sessid，sessid默认为30分钟超时。
        :return: bool
        """
        return self._openapi.update_session()

    def get_api(self, **kwargs) -> Dict[str, Any]:
        """GET接口请求

        执行OpenAPI的GET请求，并返回rquests执行结果。

        :param dict kwargs: OpenApi方法和参数集合的字典 {'method': 'user', 'domain': 'winmail.cn' .....}

        :return: Dict {result: ok/error, info: ""}
        """

        return self._openapi.get_api(**kwargs)

    def post_api(self, **kwargs) -> Dict[str, Any]:
        """POST接口请求

        执行OpenAPI的POST请求，并返回rquests执行结果。

        :param dict kwargs: OpenApi方法和参数集合的字典 {'method': 'user', 'domain': 'winmail.cn' .....}

        :return: Dict {result: ok/error, info: ""}
        """
        return self._openapi.post_api(**kwargs)

    def logout(self) -> Dict[str, Any]:
        """ 退出登陆

        退出接口登陆，清空服务器的sessid

        :return: Dict
        """

        return self._openapi.logout()
