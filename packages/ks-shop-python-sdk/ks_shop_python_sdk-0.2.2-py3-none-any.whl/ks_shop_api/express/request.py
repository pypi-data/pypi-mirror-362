# -*- coding: utf-8 -*-
from ks_shop_api.base import RestApi
"""
快递 API
"""


class OpenExpressCustomTempateListQueryRequest(RestApi):
    """
    获取自定义区模板列表
    更新时间: 2022-04-12 20:15:43
    获取自定义区模板列表

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.express.custom.tempate.list.query&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.express.custom.tempate.list.query"


class OpenExpressEbillAppendRequest(RestApi):
    """
    追加电子面单子单
    更新时间: 2023-10-30 14:45:16
    追加电子面单(暂时只支持顺丰)

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.express.ebill.append&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.express.ebill.append"


class OpenExpressEbillCancelRequest(RestApi):
    """
    取消电子面单号
    更新时间: 2023-10-30 14:59:03
    用于商家/ISV取消快手电子面单号场景

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.express.ebill.cancel&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.express.ebill.cancel"


class OpenExpressEbillGetRequest(RestApi):
    """
    获取电子面单号
    更新时间: 2024-06-13 11:49:04
    用于获取快手电子面单号，支持使用快手订单收货地址密文取号，支持批量取号（一次最多取10个）

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.express.ebill.get&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.express.ebill.get"


class OpenExpressEbillUpdateRequest(RestApi):
    """
    更新电子面单信息
    更新时间: 2023-10-30 16:54:20
    根据物流运单或更新电子面单信息

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.express.ebill.update&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.express.ebill.update"


class OpenExpressPrinterElementQueryRequest(RestApi):
    """
    获取自定义模板打印项列表
    更新时间: 2022-04-11 19:33:53
    获取自定义区模板列表

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.express.printer.element.query&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.express.printer.element.query"


class OpenExpressReachableQueryRequest(RestApi):
    """
    查询快递地址是否可达
    更新时间: 2023-10-30 19:05:41
    查询快递地址是否可达
    支持的地址类型：
    0、发货地址+收货地址
    1、发货地址
    2、收货地址

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.express.reachable.query&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.express.reachable.query"


class OpenExpressStandardTemplateListGetRequest(RestApi):
    """
    获取所有标准电子面单模板
    更新时间: 2023-10-31 10:39:02
    获取所有标准电子面单模板

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.express.standard.template.list.get&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.express.standard.template.list.get"


class OpenExpressSubscribeQueryRequest(RestApi):
    """
    查询与物流商的订购和使用信息
    更新时间: 2023-10-31 10:40:06
    查询授权商家和物流商的订购关系以及面单使用情况

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.express.subscribe.query&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.express.subscribe.query"
