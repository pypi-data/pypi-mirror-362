# -*- coding: utf-8 -*-
from ks_shop_api.base import RestApi
"""
虚拟 API
"""


class IntegrationVirtualTopupMobileOrderCallbackRequest(RestApi):
    """
    话费充值回调
    更新时间: 2024-05-23 10:27:20
    回调话费充值结果

    https://open.kwaixiaodian.com/zone/new/docs/api?name=integration.virtual.topup.mobile.order.callback&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "integration.virtual.topup.mobile.order.callback"


class OpenVirtualEticketCheckavailableRequest(RestApi):
    """
    查询电子凭证校验结果
    更新时间: 2023-11-01 20:02:42
    检查电子凭证是否有效

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.virtual.eticket.checkavailable&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.virtual.eticket.checkavailable"
