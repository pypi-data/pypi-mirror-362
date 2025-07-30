# -*- coding: utf-8 -*-
from ks_shop_api.base import RestApi
"""
发票 API
"""


class OpenInvoiceAmountGetRequest(RestApi):
    """
    查询商家开票金额
    更新时间: 2024-06-26 19:12:44
    查询商家开票金额

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.invoice.amount.get&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.invoice.amount.get"


class OpenInvoiceSubsidyAuditInfoRequest(RestApi):
    """
    国补消费者发票信息查询新接口
    更新时间: 2025-05-29 11:41:08
    国补消费者发票信息查询最新接口，可直接获取明文，无需调用解密接口

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.invoice.subsidy.audit.info&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.invoice.subsidy.audit.info"
