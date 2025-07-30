from enum import Enum


class AuthType(str, Enum):
    """用户认证类型

    internal = 内部认证
    nt = NT认证
    third_party = 第三方认证
    """
    internal = 0
    nt = 1
    third_party = 2


class UserStatus(str, Enum):
    """用户状态

    normal = 正常
    disabled = 禁止
    pending = 待审核
    paused = 暂停
    suspended = 休眠
    """

    normal = 0
    disabled = 1
    pending = 2
    paused = 3
    suspended = 4
