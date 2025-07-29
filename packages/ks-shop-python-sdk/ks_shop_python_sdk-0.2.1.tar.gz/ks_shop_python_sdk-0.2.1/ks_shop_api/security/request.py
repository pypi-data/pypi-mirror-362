# -*- coding: utf-8 -*-
from ks_shop_api.base import RestApi
"""
安全 API
"""


class OpenSecurityInstantDecryptBatchRequest(RestApi):
    """
    批量解密时效密文信息
    更新时间: 2022-07-19 14:02:41
    批量解密时效密文信息

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.security.instant.decrypt.batch&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.security.instant.decrypt.batch"


class OpenSecurityLogBatchRequest(RestApi):
    """
    日志批量上传接口
    更新时间: 2021-12-21 11:35:36
    日志批量上传接口

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.security.log.batch&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.security.log.batch"


class OpenSecurityLogLoginRequest(RestApi):
    """
    登陆日志上传接口
    更新时间: 2021-12-21 11:35:37
    自建账号体系登陆日志上传接口

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.security.log.login&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.security.log.login"


class OpenSecurityLogOpenRequest(RestApi):
    """
    开放场景订单日志上传接口
    更新时间: 2021-12-21 11:35:41
    开放场景订单日志上传接口

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.security.log.open&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.security.log.open"


class OpenSecurityLogOrderRequest(RestApi):
    """
    订单访问日志上传接口
    更新时间: 2021-12-21 11:35:41
    订单访问日志上传接口

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.security.log.order&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.security.log.order"


class OpenSecurityLogSqlRequest(RestApi):
    """
    数据库操作日志上传接口
    更新时间: 2021-12-21 11:35:38
    数据库操作日志上传接口

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.security.log.sql&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.security.log.sql"
