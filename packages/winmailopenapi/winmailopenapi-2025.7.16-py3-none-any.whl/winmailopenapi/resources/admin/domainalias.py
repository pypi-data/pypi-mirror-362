# -*- coding:utf-8 -*-

from typing import Optional, Dict, Any


class DomainAlias:
    def __init__(self, api):
        self._api = api

    def __call__(self, pageno: Optional[int] = 0) -> Dict[str, Any]:
        """ 获取域别名列表

        获取所有域别名

        :param pageno: 分页序号，以 0 开始
        :return: 成功返回值
           {
                "result": "ok",
                "info": {
                    "domainaliases": [
                        {
                            "domainid": 1,
                            "domain": "test1.com",
                            "realdomain": "test.com"
                        }
                    ],
                    "totalcount": 1,
                    "pagecount": 1
                }
            }
        """

        method_params = {"sessid": self._api.sessid, "method": "domainalias"}
        method_params.update({"pageno": str(pageno)})

        return self._api.post_api(**method_params)

    def added(self, domain: str, realdomain: str):
        """ 新增域别名

        给指定的域新增别名

        :param domain: 域名
        :param realdomain: 别名指向的实际域名
        :return: 成功返回值
            {
            "result": "ok",
            "errno": 0
            }
        """

        method_params = {"sessid": self._api.sessid, "method": "domainalias.added"}
        method_params.update({"domain": domain, "realdomain": realdomain})

        return self._api.post_api(**method_params)

    def delete(self, domain: str):
        """ 删除域别名

        删除指定域别名

        :param domain: 要删除的域别名
        :return: 成功返回值
            {
            "result": "ok",
            "errno": 0
            }
        """

        method_params = {"sessid": self._api.sessid, "method": "domainalias.delete"}
        method_params.update({"domain": domain})

        return self._api.post_api(**method_params)
