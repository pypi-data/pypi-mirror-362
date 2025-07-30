# -*- coding:utf-8 -*-
from typing import Optional, Dict, Any


class Domain:
    def __init__(self, api):
        self._api = api

    def __call__(self, pageno: Optional[int] = 0) -> Dict[str, Any]:
        """ 获取域名

        取所有域名列表

        :param pageno: 分页序号，以 0 开始
        :return: Dict
            {
            "result": "ok",
            "info":
                {
                “ domains ”: 域名列表 ,
                “ totalcount ”: 域名总数
                “ pagecount ”:  分页总数
                }
            }
        """

        method_params = {"sessid": self._api.sessid, "method": "domain"}
        method_params.update({"pageno": str(pageno)})

        return self._api.post_api(**method_params)

    def added(self, domain: str,
              description: Optional[str] = None,
              mailquota: Optional[int] = None,
              mailcount: Optional[int] = None,
              ftpquota: Optional[int] = None,
              ftpcount: Optional[int] = None,
              **kwargs: Optional[Dict]
              ) -> Dict[str, Any]:
        """ 新增域名

        新增域名接口

        :param domain: 域名
        :param description: 描述
        :param mailquota: 新邮箱默认空间大小,单位 MB
        :param mailcount: 新邮箱默认最多邮件数
        :param ftpquota: 新邮箱默认网络磁盘空间大小
        :param ftpcount: 新邮箱默认网络磁盘最多文件数
        :param kwargs: 其他可能参数
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            -1  域名数已经达到允许注册数
            1  域名新增失败
            2  相同的域名已经存在
            3  相同的域别名已经存在
            4  相同的 NT 认证域名已经存在
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self._api.sessid, "method": "domain.added"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue
            if k == "kwargs":
                method_params.update(kwargs)
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self._api.post_api(**method_params)

    def edited(self, domain: str,
               description: Optional[str] = None,
               mailquota: Optional[int] = None,
               mailcount: Optional[int] = None,
               ftpquota: Optional[int] = None,
               ftpcount: Optional[int] = None,
               **kwargs: Optional[Dict]
               ) -> Dict[str, Any]:
        """ 修改域名

        修改指定域名

        :param domain: 域名
        :param description: 描述
        :param mailquota: 新邮箱默认空间大小,单位 MB
        :param mailcount: 新邮箱默认最多邮件数
        :param ftpquota: 新邮箱默认网络磁盘空间大小
        :param ftpcount: 新邮箱默认网络磁盘最多文件数
        :param kwargs: 其他可能参数
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            错误代码：
            errno  值  含义
            1  域名修改失败
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self._api.sessid, "method": "domain.edited"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue
            if k == "kwargs":
                method_params.update(kwargs)
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self._api.post_api(**method_params)

    def delete(self, domain: str) -> Dict[str, Any]:
        """ 删除域名

        删除指定域名

        :param domain: 要删除的域名
        :return: 成功返回值
            { "result": "ok"}
            失败返回值
            { "result": "err", errno: 1}
            errno  值  含义
            -1  域名数已经达到允许注册数。
            1  域名删除失败
            2  此域名下存在邮箱，请先删除域下用户，别名和组
            3  主域名不能被删除
            99  您没有权限进行此项操作
        """

        method_params = {"sessid": self._api.sessid, "method": "domain.delete"}
        method_params.update({"domain": domain})

        return self._api.post_api(**method_params)
