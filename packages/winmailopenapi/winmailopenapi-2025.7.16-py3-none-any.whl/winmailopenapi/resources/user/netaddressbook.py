# -*- coding:utf-8 -*-
from typing import Dict, Any, Optional


class NetaddressBook:
    def __init__(self, api):
        self._api = api

    def __call__(self, pag: Optional[int] = 1) -> Dict[str, Any]:
        """ 列公共地址簿

        :param pag: 页码分页序号，以 1 开始
        :return: 返回值
                {
                "result": "ok",
                "info": {
                    "address": [
                        {
                            "uid": "b",
                            "name": "\u59d3\u540d\u4e59",
                            "email": "b@test.com",
                            "mobile": "13700001111",
                            "company": "\u4e59\u7684\u516c\u53f8\u540d",
                            "department": "\u4e59\u7684\u90e8\u95e8",
                            "jobtitle": " ",
                            "office": " ",
                            "officephone": " ",
                            "homeaddress": " ",
                            "homephone": " ",
                            "chksum": "4c9617b6ca8715663bbed4923c644df0",
                            "usertype": "sys"
                        }
                    ],
                    "totalpage": 2,
                    "addresscount": 31
                }
            }
        """

        method_params = {"sessid": self._api.sessid, "method": "netaddressbook", "pag": str(pag)}

        return self._api.post_api(**method_params)

    def display(self, netaddrid: str) -> Dict[str, Any]:
        """显示公共地址簿联系人详情

        显示公共地址簿联系人详情

        :param netaddrid: 联系人ID 	取自netaddressbook的中每个联系人的uid
        :return: Dict
        """

        method_params = {"sessid": self._api.sessid, "method": "netaddressbook.display", "netaddrid": netaddrid}

        return self._api.post_api(**method_params)

