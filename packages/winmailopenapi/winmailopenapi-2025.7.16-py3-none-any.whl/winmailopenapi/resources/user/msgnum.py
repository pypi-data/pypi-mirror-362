# -*- coding:utf-8 -*-
from typing import Dict, Any


class MsgNum:
    def __init__(self, api):
        self._api = api

    def __call__(self) -> Dict[str, Any]:
        """各邮件夹未读邮件数

        :return: 返回值
            {
            "result": "ok",
            "info": 各文件夹的未读邮件数
            }
        """
        method_params = {"sessid": self._api.sessid, "method": "msgnum"}

        return self._api.post_api(**method_params)