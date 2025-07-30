# -*- coding:utf-8 -*-
from typing import Optional, Dict, Any


class AdminUser:
    def __init__(self, api):
        self._api = api

    def __call__(self, pageno: Optional[int] = 0) -> Dict[str, Any]:
        """管理员列表

        获取管理员列表
        :param pageno:  页码  分页序号，以 0 开始
        :return: 成功返回值
            {
                "result": "ok",
                "info":
                {
                    “ users ”: 用户列表 ,
                    “ totalcount ”: 用户总数
                    “ pagecount ”:  分页总数
                }
            }
        """
        method_params = {"sessid": self._api.sessid, "method": "adminuser", "pageno": str(pageno)}

        return self._api.post_api(**method_params)

    def added(self,
              username: str,
              password: str,
              description: Optional[str],
              adminrange: Optional[str],
              usertype: Optional[int] = 0
              ) -> Dict[str, Any]:

        """新增 管理员

        :param username: 管理员用户名
        :param password: 管理员密码
        :param description: 描述
        :param adminrange: 允许管理的域 多个域名之间用分号(;)分隔；域管理员需设置
        :param usertype: 管理员类型 0 - 超级管理员；1 - 域管理员
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  管理新增失败
            2  用户名格式不正确
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self._api.sessid, "method": "adminuser.added"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self._api.post_api(**method_params)

    def edited(self,
               username: str,
               password: str,
               description: Optional[str],
               adminrange: Optional[str],
               usertype: Optional[int] = 0
               ) -> Dict[str, Any]:

        """修改管理员

        :param username: 管理员用户名
        :param password: 管理员密码
        :param description: 描述
        :param adminrange: 允许管理的域 多个域名之间用分号(;)分隔；域管理员需设置
        :param usertype: 管理员类型 0 - 超级管理员；1 - 域管理员
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  管理修改失败
            2  用户名格式不正确
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self._api.sessid, "method": "adminuser.edited"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self._api.post_api(**method_params)

    def delete(self,
               username: str
               ) -> Dict[str, Any]:
        """删除管理员

        :param username: 管理员用户名
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  管理删除失败
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self._api.sessid, "method": "adminuser.delete", "username": username}

        return self._api.post_api(**method_params)
