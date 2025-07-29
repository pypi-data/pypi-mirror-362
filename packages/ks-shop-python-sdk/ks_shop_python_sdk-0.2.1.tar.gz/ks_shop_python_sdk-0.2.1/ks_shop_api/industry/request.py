# -*- coding: utf-8 -*-
from ks_shop_api.base import RestApi
"""
行业 API
"""


class OpenIndustryTradeInSyncSpuInfoRequest(RestApi):
    """
    外部同步spu信息接口
    更新时间: 2024-02-25 18:16:40
    用于外部同步增量spu信息

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.industry.trade.in.sync.spu.info&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.industry.trade.in.sync.spu.info"


class OpenIndustryVirtualOrderDecryptRequest(RestApi):
    """
    批量解密虚拟订单
    更新时间: 2024-09-23 17:26:19
    仅用于解密虚拟发货订单密文数据为明文

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.industry.virtual.order.decrypt&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.industry.virtual.order.decrypt"


class OpenIndustryVirtualOrderDetailRequest(RestApi):
    """
    查询虚拟订单详情
    更新时间: 2024-01-16 20:30:09
    查询虚拟订单详情信息

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.industry.virtual.order.detail&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.industry.virtual.order.detail"


class OpenIndustryVirtualOrderReviewRequest(RestApi):
    """
    审核虚拟订单
    更新时间: 2023-10-31 10:58:57
    商家回传订单审核结果

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.industry.virtual.order.review&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.industry.virtual.order.review"
