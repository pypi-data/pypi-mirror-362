# -*- coding:utf-8 -*-
from typing import Dict, Any, Optional


class SystemGroup:
    def __init__(self, api):
        self._api = api

    def __call__(self, pag: Optional[int] = 1) -> Dict[str, Any]:
        """ 列系统通信组

        :param pag: 页码分页序号，以 1 开始
        :return: 返回值
        {
            "result": "ok",
            "info": {
                "group": [
                    {
                        "groupid": "everyone",
                        "name": "everyone",
                        "domain": "",
                        "fullname": "everyone@test.com",
                        "description": "",
                        "sendmailright": 3,
                        "visibleright": 0,
                        "sendervisible": 0,
                        "memberlist": "a;a-a;c112;api;1000",
                        "sendmailmember": "",
                        "managerlist": "",
                        "subgroup": [
                            "salse1"
                        ],
                        "extmembername": "",
                        "sortby": 0,
                        "orderno": 9999,
                        "localsend": 0,
                        "fromgroup": 0,
                        "rcptmember": 0,
                        "mailhost": "",
                        "syncaction": "",
                        "synctime": 1694592460,
                        "openid": "",
                        "id": 2982,
                        "groupmail": "everyone@test.com",
                        "manager": 0,
                        "sendmail": 1,
                        "listmember": true,
                        "arraymemberlist": null,
                        "subgrouplevel": 0,
                        "chksum": "0952e1dd7af352500f67524911b21a0c"
                    }
                ],
                "totalpage": 1,
                "groupcount": 7
            }
        }
        """

        method_params = {"sessid": self._api.sessid, "method": "systemgroup", "pag": str(pag)}

        return self._api.post_api(**method_params)
