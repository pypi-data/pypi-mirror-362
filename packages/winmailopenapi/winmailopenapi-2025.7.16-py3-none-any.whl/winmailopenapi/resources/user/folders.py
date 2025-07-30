# -*- coding:utf-8 -*-
from typing import Dict, Any


class Folders:
    def __init__(self, api):
        self._api = api

    def __call__(self):
        """列邮件夹

        列邮件夹
        :return: 返回值
            {
            "result": "ok",
            "info":
                {
                “private”:  个人邮件夹,
                “public”:  公共邮件夹
                “archive”:  归档邮件夹
                “label”:  标签
                }
            }
        """

        method_params = {"sessid": self._api.sessid, "method": "folders"}

        return self._api.post_api(**method_params)

    def newfolder(self, newfolder: str) -> Dict[str, Any]:
        """ 新建邮件夹

        新建邮件夹
        :param newfolder: 邮件夹名
        :return: 返回值
            { "result": "ok"}
        """
        method_params = {"sessid": self._api.sessid, "method": "folders.newfolder", "newfolder": newfolder}

        return self._api.post_api(**method_params)

    def renamefolder(self, folder: str, newfolder: str) -> Dict[str, Any]:
        """ 重命名 邮件夹

         重命名 邮件夹
        :param folder: 需要重命名的邮件夹
        :param newfolder: 新邮件夹名
        :return: 返回值
            { "result": "ok"}
        """
        method_params = {"sessid": self._api.sessid, "method": "folders.renamefolder",
                         "newfolder": newfolder, "folder": folder}

        return self._api.post_api(**method_params)

    def delfolder(self, folder: str) -> Dict[str, Any]:
        """ 删除邮件夹

        删除邮件夹
        :param optfolder: 要操作的邮件夹名
        :return: 返回值
            { "result": "ok"}
        """
        method_params = {"sessid": self._api.sessid, "method": "folders.delfolder", "folder": folder}

        return self._api.post_api(**method_params)

    def emptyfolder(self, folder: str) -> Dict[str, Any]:
        """ 清空邮件夹

        清空邮件夹
        :param optfolder: 要操作的邮件夹名
        :return: 返回值
            { "result": "ok"}
        """
        method_params = {"sessid": self._api.sessid, "method": "folders.emptyfolder", "folder": folder}

        return self._api.post_api(**method_params)
