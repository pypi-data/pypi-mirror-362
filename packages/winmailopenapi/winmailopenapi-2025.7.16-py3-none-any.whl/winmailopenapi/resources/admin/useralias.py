# -*- coding:utf-8 -*-

from typing import Optional, Dict, Any


class UserAlias:
    def __init__(self, api):
        self._api = api

    def __call__(self, domain: str, pageno: Optional[int] = 0) -> Dict[str, Any]:
        """ 获取用户别名列表

        获取指定域名下用户别名列表

        :param domain: 域名
        :param pageno: 分页序号，以 0 开始
        :return: 成功返回值
            {
            "result": "ok",
            "info": {
                "useraliases": [
                    {
                        "userid": 302,
                        "name": "afdasd",
                        "domain": "test.cn",
                        "realuser": "ad230b@test.cn",
                        "description": "",
                        "mailhost": "",
                        "syncaction": "",
                        "synctime": 1751338896
                    }
                ],
                "totalcount": 1,
                "pagecount": 1,
                "domain": "test.cn"
            }
        }
        """

        method_params = {"sessid": self._api.sessid, "method": "useralias"}
        method_params.update({"domain": domain, "pageno": str(pageno)})

        return self._api.post_api(**method_params)

    def added(self, name: str, domain: str, realuser: str, description: str):
        """ 新增用户别名

        给指定的邮箱新增邮箱别名

        :param name: 新增的邮箱别名
        :param domain: 域名
        :param realuser: 别名指向的实际邮箱地址
        :param description: 描述
        :return: 成功返回值
            {
            "result": "ok",
            "errno": 0
            }
        """

        method_params = {"sessid": self._api.sessid, "method": "useralias.added"}
        method_params.update({"domain": domain, "name": name, "realuser": realuser, "description": description})

        return self._api.post_api(**method_params)

    def edited(self, oldname: str, name: str, domain: str, realuser: str, description: str):
        """ 编辑用户别名

        编辑邮箱别名

        :param oldname: 要编辑的邮箱别名
        :param name: 新的邮箱别名
        :param domain: 域名
        :param realuser: 别名指向的实际邮箱地址
        :param description: 描述
        :return: 成功返回值
            {
            "result": "ok",
            "errno": 0
            }
        """

        method_params = {"sessid": self._api.sessid, "method": "useralias.edited"}
        method_params.update({"domain": domain, "oldname": oldname,
                              "name": name, "realuser": realuser, "description": description})

        return self._api.post_api(**method_params)

    def delete(self, name: str, domain: str):
        """ 删除用户别名

        删除邮箱别名

        :param name: 要删除的邮箱别名
        :param domain: 域名
        :return: 成功返回值
            {
            "result": "ok",
            "errno": 0
            }
        """

        method_params = {"sessid": self._api.sessid, "method": "useralias.delete"}
        method_params.update({"domain": domain, "name": name})

        return self._api.post_api(**method_params)
