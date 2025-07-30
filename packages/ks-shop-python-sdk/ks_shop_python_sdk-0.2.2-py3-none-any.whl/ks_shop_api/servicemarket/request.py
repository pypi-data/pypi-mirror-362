# -*- coding: utf-8 -*-
from ks_shop_api.base import RestApi
"""
服务市场 API
"""


class OpenServiceMarketBuyerServiceInfoRequest(RestApi):
    """
    获取买家服务关系
    更新时间: 2023-11-01 16:51:15
    获取买家服务关系

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.service.market.buyer.service.info&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.service.market.buyer.service.info"


class OpenServiceMarketOrderDetailRequest(RestApi):
    """
    获取服务市场订单详情
    更新时间: 2023-11-01 16:53:10
    获取服务市场订单详情

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.service.market.order.detail&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.service.market.order.detail"


class OpenServiceMarketOrderListRequest(RestApi):
    """
    获取服务市场订单列表
    更新时间: 2023-11-01 16:54:53
    获取服务市场订单列表

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.service.market.order.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.service.market.order.list"
