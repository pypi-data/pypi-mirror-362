# -*- coding:utf-8 -*-
from typing import Optional, Dict, Any


class Group:
    def __init__(self, api):
        self._api = api

    def __call__(self, domain: str, pageno: Optional[int] = 0) -> Dict[str, Any]:
        """取邮件组列表

        :param domain: 域名
        :param pageno: 页数
        :return: 成功返回值
            {
                "result": "ok",
                "info":
                {
                    “ groups ”: 邮箱用户列表 ,
                    “ totalcount ”: 用户总数
                    “ pagecount ”:  分页总数
                    “ domain ”:  所属域名
                }
            }
        """

        method_params = {"sessid": self._api.sessid, "method": "group"}
        method_params.update({"pageno": str(pageno), "domain": domain})

        return self._api.post_api(**method_params)

    def added(self,
              name: str,
              domain: str,
              fullname: Optional[str] = None,
              description: Optional[str] = None,
              subgroup: Optional[str] = None,
              members: Optional[str] = None,
              sendmailright: Optional[int] = 0,
              sendmailmembers: Optional[str] = None,
              managers: Optional[str] = None,
              visibleright: Optional[int] = 0,
              sendervisible: Optional[int] = 1,
              **kwargs: Optional[Dict]
              ) -> Dict[str, Any]:
        """新增邮件组

        :param name: 组名
        :param domain: 域名
        :param fullname: 组名称
        :param description: 描述
        :param subgroup: 子分组，各子分组名以分号(;)分
        :param members: 组成员  各成员名以分号(;)分隔
        :param sendmailright: 发信权限
            0 - 任何人都可以给组员发
            信；
            1 - 只有组员可以发信；
            2 - 仅指定成员可以发信；
            3 - 本域下用户可以发信
        :param sendmailmembers: 发信成员  各发信成员名以分号(;)分隔
        :param managers: 组管理员  各组管理员名以分号(;)分隔
        :param visibleright: 可见权限
            0 - 任何人可以看到此通讯组及其成员；
            1 - 任何人可以看到此通讯组；
            2 - 本域用户可以看到此通讯组及其成员；
            3 - 域用户可以看到此通讯组；
            4 - 组成员可以看到此通讯组及其成员；
            5 - 组成员可以看到此通讯组；
            6 - 只有管理员可以看到此通讯组及成员
        :param sendervisible: 发信成员可见
            0 - 没有特别可见权限；
            1 - 发信成员有相同的可见度。
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  组新增失败
            2  相同的用户已经存在
            3  相同的用户别名已经存在
            4  相同的邮件组已经存在
            101  主服务器增加用户失败
            102  主服务器上相同的用户已经存在
            103  主服务器上相同的用户别名已经存在
            104  主服务器上相同的邮件组已经存在
            99  您没有权限进行此项操作


        """

        method_params = {"sessid": self._api.sessid, "method": "group.added"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue
            if k == "kwargs":
                method_params.update(kwargs)
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self._api.post_api(**method_params)

    def edited(self,
               name: str,
               domain: str,
               fullname: Optional[str] = None,
               description: Optional[str] = None,
               subgroup: Optional[str] = None,
               members: Optional[str] = None,
               sendmailright: Optional[int] = 0,
               sendmailmembers: Optional[str] = None,
               managers: Optional[str] = None,
               visibleright: Optional[int] = 0,
               sendervisible: Optional[int] = 1,
               **kwargs: Optional[Dict]
               ) -> Dict[str, Any]:
        """新增邮件组

        :param name: 组名
        :param domain: 域名
        :param fullname: 组名称
        :param description: 描述
        :param subgroup: 子分组，各子分组名以分号(;)分
        :param members: 组成员  各成员名以分号(;)分隔
        :param sendmailright: 发信权限
            0 - 任何人都可以给组员发
            信；
            1 - 只有组员可以发信；
            2 - 仅指定成员可以发信；
            3 - 本域下用户可以发信
        :param sendmailmembers: 发信成员  各发信成员名以分号(;)分隔
        :param managers: 组管理员  各组管理员名以分号(;)分隔
        :param visibleright: 可见权限
            0 - 任何人可以看到此通讯组及其成员；
            1 - 任何人可以看到此通讯组；
            2 - 本域用户可以看到此通讯组及其成员；
            3 - 域用户可以看到此通讯组；
            4 - 组成员可以看到此通讯组及其成员；
            5 - 组成员可以看到此通讯组；
            6 - 只有管理员可以看到此通讯组及成员
        :param sendervisible: 发信成员可见
            0 - 没有特别可见权限；
            1 - 发信成员有相同的可见度。
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  组修改失败
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self._api.sessid, "method": "group.edited"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue
            if k == "kwargs":
                method_params.update(kwargs)
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self._api.post_api(**method_params)

    def addmember(self,
                  name: str,
                  domain: str,
                  groups: str) -> Dict[str, Any]:
        """增加组成员

        :param name: 组成员名
        :param domain: 组成员域名
        :param groups: 组名列表， 多个组以;分隔
        :return:  返回值
            成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  组成员增加失败
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self._api.sessid, "method": "group.addmember"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self._api.post_api(**method_params)

    def modifymember(self,
                     name: str,
                     domain: str,
                     groups: str) -> Dict[str, Any]:
        """修改组成员

        修改组成员，从系统里的其他组中删除此成员，仅是组名列表中的组成员。

        :param name: 组成员名
        :param domain: 组成员域名
        :param groups: 组名列表， 多个组以;分隔
        :return:  返回值
            成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  组成员增加失败
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self._api.sessid, "method": "group.modifymember"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self._api.post_api(**method_params)

    def delmember(self,
                  name: str,
                  domain: str,
                  groups: str) -> Dict[str, Any]:
        """删除组成员

        删除组成员，从指的组中删除此成员。

        :param name: 组成员名
        :param domain: 组成员域名
        :param groups: 组名列表， 多个组以;分隔
        :return:  返回值
            成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  组成员增加失败
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self._api.sessid, "method": "group.delmember"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self._api.post_api(**method_params)

    def delete(self, name: str, domain: str) -> Dict[str, Any]:
        """
        删除邮件组

        :param domain: 域名
        :param pageno: 页数
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  组删除失败
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self._api.sessid, "method": "group.delete"}
        method_params.update({"name": name, "domain": domain})

        return self._api.post_api(**method_params)
