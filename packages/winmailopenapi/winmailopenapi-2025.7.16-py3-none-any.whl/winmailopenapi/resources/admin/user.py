# -*- coding:utf-8 -*-
from typing import Optional, Union, Dict, Any

class User:
    def __init__(self, api):
        self._api = api

    def __call__(self, domain: str, pageno: Optional[int] = 0) -> Dict[str, Any]:
        """ 获取用户列表

        获取指定域名下用户列表

        :param domain: 域名
        :param pageno: 分页序号，以 0 开始
        :return: 成功返回值
            {
            "result": "ok",
            "info":
                {
                “ users ”: 邮箱用户列表 ,
                “ totalcount ”: 用户总数
                “ pagecount ”:  分页总数
                “ domain ”:  所属域名
                }
            }
        """

        method_params = {"sessid": self._api.sessid, "method": "user"}
        method_params.update({"domain": domain, "pageno": str(pageno)})

        return self._api.post_api(**method_params)

    def added(self, name: str,
              domain: str,
              password: str,
              authtype: int = 0,
              status: int = 0,
              fullname: Optional[str] = None,
              description: Optional[str] = None,
              homeaddress: Optional[str] = None,
              homephone: Optional[str] = None,
              mobile: Optional[str] = None,
              company: Optional[str] = None,
              department: Optional[str] = None,
              jobtitle: Optional[str] = None,
              office: Optional[str] = None,
              officephone: Optional[str] = None,
              mailquota: Optional[int] = None,
              mailcount: Optional[int] = None,
              ftpquota: Optional[int] = None,
              ftpcount: Optional[int] = None,
              **kwargs: Optional[Dict]
              ) -> Dict[str, Any]:
        """ 新增用户

        管理员新增邮箱用户接口。

        :param name: 邮箱用户名
        :param domain: 域名
        :param password: 邮箱密码
        :param authtype: 认证方式 0 - 本系统认证； 1 - NT 域认证； 2 - 第三方认证
        :param status: 状态 0 - 正常；1 - 禁止；2 - 等待审核
        :param fullname: 用户姓名
        :param description: 描述
        :param homeaddress: 家庭地址
        :param homephone: 电话电话
        :param mobile: 手机
        :param company: 工作单位
        :param department: 部门
        :param jobtitle: 职位
        :param office: 办公室
        :param officephone: 办公电话
        :param mailquota: 邮箱空间大小 单位MB
        :param mailcount: 邮箱最多邮件数
        :param ftpquota: 网络磁盘空间大小 单位MB
        :param ftpcount: 网络磁盘最多文件数
        :param kwargs: 其他参数
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            -1  用户数已经达到允许注册数
            1  用户新增失败
            2  相同的用户已经存在
            3  相同的用户别名已经存在
            4  相同的邮件组已经存在
            6  此域下用户邮箱数已经达到本域允许的注册数
            7  此域下用户邮箱容量已经达到本域允许的总容量
            8  此域下用户网络磁盘容量已经达到本域允许的总容量
            101  主服务器增加用户失败
            102  主服务器上相同的用户已经存在
            103  主服务器上相同的用户别名已经存在
            104  主服务器上相同的邮件组已经存在
            99  您没有权限进行此项操作
        """
        method_params = {"sessid": self._api.sessid, "method": "user.added"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue
            if k == "kwargs":
                method_params.update(kwargs)
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self._api.post_api(**method_params)

    def edited(self, name: str,
               domain: str,
               password: Optional[str] = None,
               changedpwd: Optional[int] = 0,
               authtype: int = 0,
               status: int = 0,
               fullname: Optional[str] = None,
               description: Optional[str] = None,
               homeaddress: Optional[str] = None,
               homephone: Optional[str] = None,
               mobile: Optional[str] = None,
               company: Optional[str] = None,
               department: Optional[str] = None,
               jobtitle: Optional[str] = None,
               office: Optional[str] = None,
               officephone: Optional[str] = None,
               mailquota: Optional[int] = None,
               mailcount: Optional[int] = None,
               ftpquota: Optional[int] = None,
               ftpcount: Optional[int] = None,
               **kwargs: Optional[Dict]
               ) -> Dict[str, Any]:
        """ 修改用户

        管理员修改邮箱用户接口。*如果要修改密码，增加参数 changedpwd ，值设置为 1

        :param name: 邮箱用户名
        :param domain: 域名
        :param password: 邮箱密码
        :param changedpwd: 是否修改密码
        :param authtype: 认证方式 0 - 本系统认证； 1 - NT 域认证； 2 - 第三方认证
        :param status: 状态 0 - 正常；1 - 禁止；2 - 等待审核
        :param fullname: 用户姓名
        :param description: 描述
        :param homeaddress: 家庭地址
        :param homephone: 电话电话
        :param mobile: 手机
        :param company: 工作单位
        :param department: 部门
        :param jobtitle: 职位
        :param office: 办公室
        :param officephone: 办公电话
        :param mailquota: 邮箱空间大小 单位MB
        :param mailcount: 邮箱最多邮件数
        :param ftpquota: 网络磁盘空间大小 单位MB
        :param ftpcount: 网络磁盘最多文件数
        :param kwargs: 其他参数
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  用户修改失败
            99  您没有权限进行此项操作
        """
        method_params = {"sessid": self._api.sessid, "method": "user.edited"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue
            if k == "kwargs":
                method_params.update(kwargs)
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self._api.post_api(**method_params)

    def delete(self, name: str, domain: str) -> Dict[str, Any]:
        """删除用户

        删除邮箱用户
        :param name: 邮箱用户名
        :param domain: 域名
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  用户删除失败
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self._api.sessid, "method": "user.delete"}
        method_params.update({"name": name, "domain": domain})

        return self._api.post_api(**method_params)
