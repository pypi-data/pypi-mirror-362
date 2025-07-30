# -*- coding: utf-8 -*-
from ks_shop_api.base import RestApi
"""
营销 API
"""


class OpenPromotionCouponCreateRequest(RestApi):
    """
    创建商家券
    更新时间: 2025-02-13 15:52:36
    开放平台创建营销商家券

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.promotion.coupon.create&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.promotion.coupon.create"


class OpenPromotionCouponDeleteRequest(RestApi):
    """
    删除优惠券
    更新时间: 2025-02-13 15:52:19
    只有结束优惠券才能删除优惠券

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.promotion.coupon.delete&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.promotion.coupon.delete"


class OpenPromotionCouponOverRequest(RestApi):
    """
    结束优惠券
    更新时间: 2025-02-13 15:43:59
    结束优惠券

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.promotion.coupon.over&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.promotion.coupon.over"


class OpenPromotionCouponPageListRequest(RestApi):
    """
    优惠券列表
    更新时间: 2025-02-13 15:28:28
    b端优惠券列表

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.promotion.coupon.page.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.promotion.coupon.page.list"


class OpenPromotionCouponQueryRequest(RestApi):
    """
    优惠券查询
    更新时间: 2025-02-13 15:32:57
    优惠券查询

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.promotion.coupon.query&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.promotion.coupon.query"


class OpenPromotionCouponSendRequest(RestApi):
    """
    优惠券发放
    更新时间: 2025-02-13 15:43:18
    给特定用户定向发放已创建好的优惠券，发放渠道为创建优惠券时可支持的渠道

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.promotion.coupon.send&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.promotion.coupon.send"


class OpenPromotionCouponStatisticRequest(RestApi):
    """
    查询优惠券使用详情
    更新时间: 2025-02-13 15:51:20
    根据优惠券id查询优惠券的使用和消耗统计信息

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.promotion.coupon.statistic&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.promotion.coupon.statistic"


class OpenPromotionCouponStockAddRequest(RestApi):
    """
    修改券库存
    更新时间: 2025-02-13 15:43:01
    修改商家券库存

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.promotion.coupon.stock.add&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.promotion.coupon.stock.add"


class OpenPromotionCrowdCreateRequest(RestApi):
    """
    新建人群包
    更新时间: 2024-11-07 22:01:34
    新建人群包

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.promotion.crowd.create&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.promotion.crowd.create"


class OpenPromotionCrowdDetailRequest(RestApi):
    """
    获取人群包详情
    更新时间: 2024-06-07 15:19:41
    获取人群包详情

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.promotion.crowd.detail&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.promotion.crowd.detail"


class OpenPromotionCrowdEditRequest(RestApi):
    """
    编辑人群包
    更新时间: 2023-07-13 11:19:28
    编辑人群包

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.promotion.crowd.edit&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.promotion.crowd.edit"


class OpenPromotionCrowdPredictRequest(RestApi):
    """
    预估人群包圈选数量
    更新时间: 2023-07-13 11:18:44
    预估人群包圈选数量

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.promotion.crowd.predict&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.promotion.crowd.predict"


class OpenPromotionSellerStatisticRequest(RestApi):
    """
    查看商家的优惠券数据
    更新时间: 2025-02-13 15:52:00
    获取商家的x天内统计数据

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.promotion.seller.statistic&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.promotion.seller.statistic"


class OpenPromotionShopNewbieCreateRequest(RestApi):
    """
    创建店铺新人券
    更新时间: 2025-02-13 15:52:46
    创建店铺新人券

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.promotion.shop.newbie.create&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.promotion.shop.newbie.create"
