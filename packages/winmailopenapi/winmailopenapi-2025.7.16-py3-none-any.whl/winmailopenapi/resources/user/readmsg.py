from typing import Dict, Any


class ReadMsg:
    def __init__(self, api):
        self._api = api

    def __call__(self, folder: str, msgid: int) -> Dict[str, Any]:
        """ 阅读邮件

        :param folder: 文件夹
        :param msgid: 邮件标识
        :return: 返回值
            {
            "result": "ok",
            "info":
                {
                “from”:  发件人信息,
                “reply-to”: 回复信息
                “to”:  收件人信息
                “cc”:  抄送信息
                “subject”: 主题
                “date”:  发件日期
                “body”:  信体内容
                “attachment”:  邮件附件
                “memo”:  邮件备注信息
                }
            }
        """
        method_params = {"sessid": self._api.sessid, "method": "readmsg", "folder": folder, "msgid": str(msgid)}

        return self._api.post_api(**method_params)
