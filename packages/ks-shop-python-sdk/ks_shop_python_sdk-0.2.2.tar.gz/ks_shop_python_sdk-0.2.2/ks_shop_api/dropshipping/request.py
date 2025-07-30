# -*- coding: utf-8 -*-
from ks_shop_api.base import RestApi
"""
代发 API
"""


class OpenDropshippingEbillBatchGetRequest(RestApi):
    """
    代发订单电子面单批量取号
    更新时间: 2023-10-30 14:21:53
    代发订单电子面单批量取号（最多10个）

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.dropshipping.ebill.batch.get&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.dropshipping.ebill.batch.get"


class OpenDropshippingEbillCancelRequest(RestApi):
    """
    代发订单电子面单取消
    更新时间: 2023-10-30 12:03:40
    代发订单电子面单取消

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.dropshipping.ebill.cancel&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.dropshipping.ebill.cancel"


class OpenDropshippingOrderBatchAllocateRequest(RestApi):
    """
    商家批量分配代发订单
    更新时间: 2023-10-30 12:02:23
    商家给已建立代发关系的厂家分配代发订单

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.dropshipping.order.batch.allocate&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.dropshipping.order.batch.allocate"


class OpenDropshippingOrderBatchAllocateCancelRequest(RestApi):
    """
    商家批量取消分配代发订单
    更新时间: 2023-11-22 13:36:19
    商家取消已分配给厂家的代发订单

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.dropshipping.order.batch.allocate.cancel&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.dropshipping.order.batch.allocate.cancel"


class OpenDropshippingOrderBatchAppendRequest(RestApi):
    """
    商家批量追加代发订单
    更新时间: 2022-11-30 20:11:11
    商家基于交易主单追加代发订单，举例场景：赠品、补货、换货、其它等

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.dropshipping.order.batch.append&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.dropshipping.order.batch.append"


class OpenDropshippingOrderBatchDeleteRequest(RestApi):
    """
    商家批量删除代发订单
    更新时间: 2022-11-30 20:07:49
    【商家端】商家批量删除代发订单

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.dropshipping.order.batch.delete&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.dropshipping.order.batch.delete"


class OpenDropshippingOrderDeliverRequest(RestApi):
    """
    代发订单发货
    更新时间: 2024-10-31 16:03:18
    代发订单发货

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.dropshipping.order.deliver&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.dropshipping.order.deliver"


class OpenDropshippingOrderDetailQueryRequest(RestApi):
    """
    获取代发订单详情
    更新时间: 2025-01-21 13:07:38
    获取代发订单详情

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.dropshipping.order.detail.query&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.dropshipping.order.detail.query"


class OpenDropshippingOrderListRequest(RestApi):
    """
    获取代发订单列表
    更新时间: 2025-01-21 13:07:13
    获取代发订单列表

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.dropshipping.order.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.dropshipping.order.list"


class OpenDropshippingOrderLogisticsUpdateRequest(RestApi):
    """
    代发订单更新运单号
    更新时间: 2023-10-30 14:39:13
    代发订单更新运单号

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.dropshipping.order.logistics.update&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.dropshipping.order.logistics.update"


class OpenDropshippingOrderMerchantDetailRequest(RestApi):
    """
    商家获取代发订单详情
    更新时间: 2024-06-18 20:46:58
    【商家端】商家主动查询自己的代发订单详情

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.dropshipping.order.merchant.detail&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.dropshipping.order.merchant.detail"


class OpenDropshippingOrderMerchantListRequest(RestApi):
    """
    商家获取代发订单列表
    更新时间: 2022-11-30 20:10:39
    【商家端】商家主动拉取需要代发的订单列表信息

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.dropshipping.order.merchant.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.dropshipping.order.merchant.list"


class OpenDropshippingRelationListRequest(RestApi):
    """
    商家获取商家与厂家代发关系列表
    更新时间: 2023-10-30 14:40:37
    【商家端】商家主动拉取其与厂家的所有绑定关系数据（包括申请中、已解绑等）

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.dropshipping.relation.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.dropshipping.relation.list"


class OpenDropshippingRelationMerchantBatchApplyRequest(RestApi):
    """
    商家批量申请绑定厂家
    更新时间: 2023-10-30 14:42:23
    【商家端】商家线上申请与厂家建立代发绑定关系

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.dropshipping.relation.merchant.batch.apply&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.dropshipping.relation.merchant.batch.apply"


class OpenDropshippingRelationMerchantBatchUnbindRequest(RestApi):
    """
    商家批量解绑厂家
    更新时间: 2022-11-30 20:09:58
    商家线上解除与厂家建立的代发绑定关系（

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.dropshipping.relation.merchant.batch.unbind&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.dropshipping.relation.merchant.batch.unbind"


class OpenDropshippingRoleQueryRequest(RestApi):
    """
    代发用户查询身份类型
    更新时间: 2022-12-14 21:10:28
    代发用户查询身份类型，身份类型包括：
    0.未知身份；
    1.商家；
    2.厂家

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.dropshipping.role.query&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.dropshipping.role.query"
