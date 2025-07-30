# -*- coding:utf-8 -*-
from typing import Dict, Any, Union


class Upload:
    def __init__(self, api):
        self._api = api

    def __call__(self):
        raise AttributeError("Direct execution is not supported for this method. Check the API manual.")

    def upload(self, attachfile: Union[str, list]) -> Dict[str, Any]:
        """上传附件

        可以一次上传多个文件，也可以分多次上传, 附件文件绝对路径。
        :param attachfile: 附件文件绝对路径或者多附件List。
        :return: 返回值
            {
            "result": "ok",
            “list”:[
                    {
                    "name":"readme.txt",
                    "dispname":"readme.txt",
                    "localname":"C:\\Winmail\\server\\webmail\\temp\\_attachments\\test_baa065a52e385
                    9e4e1a0ee2ca9188713_3a077176425dd745941ee40cd3dc5914",
                    "type":"text/plain",
                    "size":156894
                    },
                    {
                    "name":" 20180705141449.jpg",
                    "dispname":" 20180705141449.jpg",
                    "localname":"C:\\Winmail\\server\\webmail\\temp\\_attachments\\test_baa065a52e385
                    9e4e1a0ee2ca9188713_ 052c4b360ca824741aaa873077e8570d",
                    "type":"image/jpg",
                    "size": 54954
                    }
            ]
            }
        """

        method_params = {"sessid": self._api.sessid, "method": "upload.upload", "attachfile": attachfile}

        return self._api.post_api(**method_params)

    def delete(self, attachid: int) -> Dict[str, Any]:
        """删除某个附件

        :param attachid: 附件 ID。上传后返回的附件数组， 所删除附件在数组中序号，序号以 0 开始
        :return: 返回值{ "result": "ok"}
        """

        method_params = {"sessid": self._api.sessid, "method": "upload.delete", "attachid": attachid}

        return self._api.post_api(**method_params)
