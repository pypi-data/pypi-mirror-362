from typing import Dict, Any, Optional


class NewMsg:
    def __init__(self, api):
        self._api = api

    def __call__(self):
        raise AttributeError("Direct execution is not supported for this method. Check the API manual.")

    def send(self, to: str,
             subject: str,
             msgbody: str,
             cc: Optional[str] = '',
             ishtml: Optional[int] = 1,
             priority: Optional[int] = 0,
             requestnotify: Optional[int] = 0,
             savetosent: Optional[int] = 1,
             splitrcpt: Optional[int] = 0,
             sendutf8: Optional[int] = 1,
             **kwargs
             ) -> Dict[str, Any]:
        """ 发送邮件

        如果要发送带附件的邮件，要先重置写邮件缓存，然后上传附件，最后再发送邮件。重置写邮件缓存，如要发送含附件邮件建议先进行重置操作。
        :param to: 收件人 多个地址用分号(;)分隔
        :param cc: 抄送 多个地址用分号(;)分隔
        :param subject: 邮件主题
        :param msgbody: 邮件信体
        :param ishtml: Html 邮件  0 - 文本邮件；1 – HTML 邮件
        :param priority: 优先级  0 - 正常；1 - 优先
        :param requestnotify: 请求阅读回条 0 - 不需要；1 - 需要
        :param savetosent: 0 - 不需要；1 - 需要
        :param splitrcpt: 0 - 不需要；1 - 需要
        :param sendutf8: 0 - 不需要；1 - 需要
        :return: 返回值 { "result": "ok"}
        """
        method_params = {"sessid": self._api.sessid, "method": "newmsg.send"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue
            if k == "kwargs":
                method_params.update(kwargs)
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self._api.post_api(**method_params)

    def reset(self) -> Dict[str, Any]:
        """ 重置写邮件缓存

        :return: 返回值 { "result": "ok"}
        """
        method_params = {"sessid": self._api.sessid, "method": "newmsg.reset"}

        return self._api.post_api(**method_params)
