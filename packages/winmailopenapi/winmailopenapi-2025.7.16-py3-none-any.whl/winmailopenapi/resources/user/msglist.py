# -*- coding:utf-8 -*-
from typing import Dict, Any, Optional


class MsgList:
    def __init__(self, api):
        self._api = api

    def __call__(self, folder: str, pag: Optional[int] = 1, **kwargs) -> Dict[str, Any]:
        """列邮件夹的邮件

        列邮件夹的邮件，此接口还有listtype/label参数，以便列出已读未读之类特定邮件。
        | listtype值 |                                       |
        | ---------- | ------------------------------------- |
        | flagged    | 星标邮件                              |
        | read       | 已读                                  |
        | unread     | 未读                                  |
        | answered   | 已回复                                |
        | forwarded  | 已转发                                |
        | label      | 有标签（需要和另一个参数label同时用） |

        :param folder: 文件夹
        :param pag: 页码 分页序号，以 1 开始
        :return: 返回值
        {
        "result": "ok",
        "info":
            {
            “messagelist”:  邮件列表信息,
            “totalpage”:  总分页数
            “newmsg”:  新邮件数
            “msgtotal”:  邮件总数
            }
        }
        """
        method_params = {"sessid": self._api.sessid, "method": "msglist"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue
            if k == "kwargs":
                method_params.update(kwargs)
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self._api.post_api(**method_params)

    def delete(self, folder: str, msgid: int) -> Dict[str, Any]:
        """删除邮件

        :param folder: 文件夹
        :param msgid: 邮件标识
        :return: 返回值{ "result": "ok"}
        """
        method_params = {"sessid": self._api.sessid, "method": "msglist.delete", "folder": folder, "msgid": msgid}

        return self._api.post_api(**method_params)

    def move(self, folder: str, msgid: int, tofolder: str) -> Dict[str, Any]:
        """删除邮件

        :param folder: 文件夹
        :param msgid: 邮件标识
        :param tofolder:  目标邮件夹
        :return: 返回值{ "result": "ok"}
        """
        method_params = {"sessid": self._api.sessid, "method": "msglist.move",
                         "folder": folder, "msgid": msgid, "tofolder": tofolder}

        return self._api.post_api(**method_params)

    def top(self, folder: str, msgid: int) -> Dict[str, Any]:
        """置顶邮件

        :param folder: 文件夹
        :param msgid: 邮件标识
        :return: 返回值{ "result": "ok"}
        """
        method_params = {"sessid": self._api.sessid, "method": "msglist.top", "folder": folder, "msgid": msgid}

        return self._api.post_api(**method_params)

    def untop(self, folder: str, msgid: int) -> Dict[str, Any]:
        """取消置顶邮件

        :param folder: 文件夹
        :param msgid: 邮件标识
        :return: 返回值{ "result": "ok"}
        """
        method_params = {"sessid": self._api.sessid, "method": "msglist.untop", "folder": folder, "msgid": msgid}

        return self._api.post_api(**method_params)

    def read(self, folder: str, msgid: int) -> Dict[str, Any]:
        """邮件标记已读

        :param folder: 文件夹
        :param msgid: 邮件标识
        :return: 返回值{ "result": "ok"}
        """
        method_params = {"sessid": self._api.sessid, "method": "msglist.read", "folder": folder, "msgid": msgid}

        return self._api.post_api(**method_params)

    def unread(self, folder: str, msgid: int) -> Dict[str, Any]:
        """邮件标记未读

        :param folder: 文件夹
        :param msgid: 邮件标识
        :return: 返回值{ "result": "ok"}
        """
        method_params = {"sessid": self._api.sessid, "method": "msglist.unread", "folder": folder, "msgid": msgid}

        return self._api.post_api(**method_params)

    def flag(self, folder: str, msgid: int) -> Dict[str, Any]:
        """设置星标邮件

        :param folder: 文件夹
        :param msgid: 邮件标识
        :return: 返回值{ "result": "ok"}
        """
        method_params = {"sessid": self._api.sessid, "method": "msglist.flag", "folder": folder, "msgid": msgid}

        return self._api.post_api(**method_params)

    def unflag(self, folder: str, msgid: int) -> Dict[str, Any]:
        """取消星标邮件

        :param folder: 文件夹
        :param msgid: 邮件标识
        :return: 返回值{ "result": "ok"}
        """
        method_params = {"sessid": self._api.sessid, "method": "msglist.unflag", "folder": folder, "msgid": msgid}

        return self._api.post_api(**method_params)
