# -*- coding:utf-8 -*-
from typing import Dict, Optional, Any


class AddressBook:
    def __init__(self, api):
        self._api = api

    def __call__(self, pag: Optional[int] = 1) -> Dict[str, Any]:
        """ 列个人地址簿

        :param pag: 页码分页序号，以 1 开始
        :return: 返回值
                {
                "result": "ok",
                "info":
                    {
                    “group”:  地址组列表 ,
                    “address”:  联系人列表
                    “totalpage”:  总页数
                    “addresscount”:  邮件总数
                    }
                }
        """

        method_params = {"sessid": self._api.sessid, "method": "addressbook", "pag": str(pag)}

        return self._api.post_api(**method_params)

    def addcontact(self, name: str, email: str,
                   mobile: Optional[str] = '',
                   phone: Optional[str] = '',
                   fax: Optional[str] = '',
                   address: Optional[str] = '',
                   zipcode: Optional[str] = '',
                   company: Optional[str] = '',
                   depart: Optional[str] = '',
                   jobtitle: Optional[str] = '',
                   homephone: Optional[str] = '',
                   homeaddress: Optional[str] = '',
                   homezipcode: Optional[str] = '',
                   im: Optional[str] = '',
                   url: Optional[str] = '',
                   email1: Optional[str] = '',
                   birthday: Optional[str] = '',
                   memo: Optional[str] = '') -> Dict[str, Any]:
        """ 增加联系人

         增加个人地址簿联系人
        :param name: 姓名
        :param email: 邮件地址
        :param mobile: 手机
        :param phone: 电话
        :param fax: 传真
        :param address: 联系地址
        :param zipcode: 区号
        :param company: 工作单位
        :param depart: 部门
        :param jobtitle: 职位
        :param homephone: 家庭电话
        :param homeaddress: 家庭地址
        :param homezipcode: 家庭区号
        :param im: 即时通信
        :param url: 个人网址
        :param email1: 备份邮箱地址
        :param birthday: 生日
        :param memo: 备注
        :return: 返回值{ "result": "ok"}
        """

        method_params = {"sessid": self._api.sessid, "method": "addressbook.addcontact"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self._api.post_api(**method_params)

    def savecontact(self, id: int, name: str, email: str,
                    mobile: Optional[str] = '',
                    phone: Optional[str] = '',
                    fax: Optional[str] = '',
                    address: Optional[str] = '',
                    zipcode: Optional[str] = '',
                    company: Optional[str] = '',
                    depart: Optional[str] = '',
                    jobtitle: Optional[str] = '',
                    homephone: Optional[str] = '',
                    homeaddress: Optional[str] = '',
                    homezipcode: Optional[str] = '',
                    im: Optional[str] = '',
                    url: Optional[str] = '',
                    email1: Optional[str] = '',
                    birthday: Optional[str] = '',
                    memo: Optional[str] = '') -> Dict[str, Any]:
        """ 修改 联系人

        :param id: 联系人标识
        :param name: 姓名
        :param email: 邮件地址
        :param mobile: 手机
        :param phone: 电话
        :param fax: 传真
        :param address: 联系地址
        :param zipcode: 区号
        :param company: 工作单位
        :param depart: 部门
        :param jobtitle: 职位
        :param homephone: 家庭电话
        :param homeaddress: 家庭地址
        :param homezipcode: 家庭区号
        :param im: 即时通信
        :param url: 个人网址
        :param email1: 备份邮箱地址
        :param birthday: 生日
        :param memo: 备注
        :return: 返回值{ "result": "ok"}
        """

        method_params = {"sessid": self._api.sessid, "method": "addressbook.savecontact"}
        for k, v in locals().items():
            if k in ["self", 'k', 'v', 'method_params']:
                continue

            if v is not None:
                method_params.update({k: str(v) if isinstance(v, int) else v})

        return self._api.post_api(**method_params)

    def delecontact(self, id: int) -> Dict[str, Any]:
        """ 删除 联系人

        :param id: 联系人标识
        :return: { "result": "ok"}
        """
        method_params = {"sessid": self._api.sessid, "method": "addressbook.delecontact", "id": str(id)}

        return self._api.post_api(**method_params)

    def addgroup(self, name: str, member: str) -> Dict[str, Any]:
        """增加地址组

        :param name: 分组名称
        :param member: 组成员多个联系人地址用分号(;)分隔
        :return: { "result": "ok"}
        """

        method_params = {"sessid": self._api.sessid, "method": "addressbook.addgroup",
                         "name": name, "member": member}

        return self._api.post_api(**method_params)

    def savegroup(self, id: int, name: str, member: str) -> Dict[str, Any]:
        """修改地址组

        :param id: 组标识
        :param name: 分组名称
        :param member: 组成员多个联系人地址用分号(;)分隔
        :return: { "result": "ok"}
        """

        method_params = {"sessid": self._api.sessid, "method": "addressbook.savegroup", "id": str(id),
                         "name": name, "member": member}

        return self._api.post_api(**method_params)

    def delegroup(self, id: int) -> Dict[str, Any]:
        """ 删除地址组

        :param id: 组标识
        :return: { "result": "ok"}
        """
        method_params = {"sessid": self._api.sessid, "method": "addressbook.delegroup", "id": str(id)}

        return self._api.post_api(**method_params)
