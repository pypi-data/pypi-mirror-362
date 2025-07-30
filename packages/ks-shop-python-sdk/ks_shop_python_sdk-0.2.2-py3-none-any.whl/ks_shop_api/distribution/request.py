# -*- coding: utf-8 -*-
import deprecation
from ks_shop_api.base import RestApi
"""
快分销 API
"""


class OpenDistributionCpsClipmcnOrderDetailRequest(RestApi):
    """
    getMcnOrderDetail
    更新时间: 2025-06-12 21:25:36
    获取二创机构订单详情

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.clipmcn.order.detail&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.clipmcn.order.detail"


class OpenDistributionCpsClipmcnOrderListRequest(RestApi):
    """
    listMcnOrder
    更新时间: 2025-06-12 19:16:05
    二创订单列表查询

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.clipmcn.order.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.clipmcn.order.list"


class OpenDistributionCpsDistributorOrderCommentListRequest(RestApi):
    """
    分销达人推广订单评论（批量）
    更新时间: 2021-12-30 15:34:35
    分销达人推广订单评论（批量）

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.distributor.order.comment.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.distributor.order.comment.list"


class OpenDistributionCpsDistributorOrderCursorListRequest(RestApi):
    """
    分销达人推广订单列表(游标方式)
    更新时间: 2025-04-29 17:20:12
    分销达人推广订单列表(游标方式)
    24.10.15 新增上线 出参cpsOrderStatus分销订单状态＝40为已发货。若之前使用其他方案判断已发货，请尽快更新逻辑进行兼容，并更新数据，以防使用有误。

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.distributor.order.cursor.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.distributor.order.cursor.list"


class OpenDistributionCpsKwaimoneyLinkCreateRequest(RestApi):
    """
    创建快赚客推广链接
    更新时间: 2024-06-04 10:41:22
    创建快赚客推广链接

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.kwaimoney.link.create&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.kwaimoney.link.create"


class OpenDistributionCpsKwaimoneyLinkParseRequest(RestApi):
    """
    解析快赚客分享口令
    更新时间: 2024-05-22 15:06:08
    解析快赚客分享口令

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.kwaimoney.link.parse&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.kwaimoney.link.parse"


class OpenDistributionCpsKwaimoneyLinkTransferRequest(RestApi):
    """
    快赚客转链转化接口
    更新时间: 2023-06-29 10:14:47
    快赚客转链转化接口

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.kwaimoney.link.transfer&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.kwaimoney.link.transfer"


class OpenDistributionCpsKwaimoneyNewPromotionEffectDetailRequest(RestApi):
    """
    查询快赚客拉新推广效果数据明细
    更新时间: 2023-04-26 18:19:25
    查询快赚客拉新推广效果数据明细

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.kwaimoney.new.promotion.effect.detail&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.kwaimoney.new.promotion.effect.detail"


class OpenDistributionCpsKwaimoneyNewPromotionEffectTrendRequest(RestApi):
    """
    查询快赚客拉新推广效果趋势数据
    更新时间: 2023-03-17 15:19:36
    查询快赚客拉新推广效果趋势数据

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.kwaimoney.new.promotion.effect.trend&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.kwaimoney.new.promotion.effect.trend"


class OpenDistributionCpsKwaimoneyOrderDetailRequest(RestApi):
    """
    站外分销快赚客订单详情查询
    更新时间: 2024-10-17 19:38:02
    站外分销快赚客订单详情查询

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.kwaimoney.order.detail&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.kwaimoney.order.detail"


class OpenDistributionCpsKwaimoneyOrderListRequest(RestApi):
    """
    查询快赚客分销订单
    更新时间: 2024-10-17 19:37:51
    快赚客获取分销推广订单

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.kwaimoney.order.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.kwaimoney.order.list"


class OpenDistributionCpsKwaimoneyPidCreateRequest(RestApi):
    """
    创建快赚客推广位
    更新时间: 2024-05-22 15:12:50
    创建快赚客推广位

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.kwaimoney.pid.create&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.kwaimoney.pid.create"


class OpenDistributionCpsKwaimoneyPidListRequest(RestApi):
    """
    查询快赚客推广位
    更新时间: 2024-05-22 15:13:04
    查询快赚客推广位

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.kwaimoney.pid.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.kwaimoney.pid.list"


class OpenDistributionCpsKwaimoneyPidUpdateRequest(RestApi):
    """
    更新快赚客推广位
    更新时间: 2024-05-22 15:13:19
    更新快赚客推广位

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.kwaimoney.pid.update&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.kwaimoney.pid.update"


class OpenDistributionCpsKwaimoneySelectionChannelListRequest(RestApi):
    """
    获取站外分销选品频道列表
    更新时间: 2021-12-22 17:10:03
    获取站外分销选品频道列表

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.kwaimoney.selection.channel.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.kwaimoney.selection.channel.list"


class OpenDistributionCpsKwaimoneySelectionItemDetailRequest(RestApi):
    """
    获取站外分销商品详情
    更新时间: 2024-04-08 14:29:46
    获取站外分销商品详情

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.kwaimoney.selection.item.detail&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.kwaimoney.selection.item.detail"


class OpenDistributionCpsKwaimoneySelectionItemListRequest(RestApi):
    """
    获取站外分销商品列表
    更新时间: 2025-05-27 11:48:59
    获取站外分销商品列表

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.kwaimoney.selection.item.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.kwaimoney.selection.item.list"


class OpenDistributionCpsLeaderOrderCursorListRequest(RestApi):
    """
    分销团长订单列表(游标方式)
    更新时间: 2025-06-10 21:54:36
    分销团长订单列表(游标方式)
    24.10.15 新增上线 出参cpsOrderStatus分销订单状态＝40为已发货。若之前使用其他方案判断已发货，请尽快更新逻辑进行兼容，并更新数据，以防使用有误。

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.leader.order.cursor.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.leader.order.cursor.list"


class OpenDistributionCpsLeaderOrderDetailRequest(RestApi):
    """
    分销团长订单详情
    更新时间: 2025-04-29 17:21:02
    分销团长订单详情
    24.10.15 新增上线 出参cpsOrderStatus分销订单状态＝40为已发货。若之前使用其他方案判断已发货，请尽快更新逻辑进行兼容，并更新数据，以防使用有误。

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.leader.order.detail&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.leader.order.detail"


class OpenDistributionCpsLinkCreateRequest(RestApi):
    """
    推广链接创建接口
    更新时间: 2021-12-30 15:33:30
    推广链接创建接口

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.link.create&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.link.create"


class OpenDistributionCpsPidCreateRequest(RestApi):
    """
    推广位创建接口
    更新时间: 2021-12-30 15:36:14
    推广位创建接口

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.pid.create&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.pid.create"


class OpenDistributionCpsPidQueryRequest(RestApi):
    """
    推广位查询接口
    更新时间: 2021-12-30 15:35:56
    推广位查询接口

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.pid.query&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.pid.query"


class OpenDistributionCpsPromoterOrderDetailRequest(RestApi):
    """
    分销达人订单详情
    更新时间: 2025-04-29 17:20:36
    分销达人订单详情
    24.10.15 新增上线 出参cpsOrderStatus分销订单状态＝40为已发货。若之前使用其他方案判断已发货，请尽快更新逻辑进行兼容，并更新数据，以防使用有误。

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.promoter.order.detail&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.promoter.order.detail"


class OpenDistributionCpsPromotionBrandThemeBrandListRequest(RestApi):
    """
    获取品牌好货品牌列表
    更新时间: 2022-06-29 14:05:27
    平台运营人员根据专题模块属性不同，人工招商后，配置的商品

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.promotion.brand.theme.brand.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.promotion.brand.theme.brand.list"


class OpenDistributionCpsPromotionBrandThemeItemListRequest(RestApi):
    """
    获取品牌好货品牌商品
    更新时间: 2021-12-30 16:11:46
    平台运营人员根据专题模块属性不同，人工招商后，配置的商品

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.promotion.brand.theme.item.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.promotion.brand.theme.item.list"


class OpenDistributionCpsPromotionBrandThemeListRequest(RestApi):
    """
    获取品牌好货专题列表
    更新时间: 2021-12-30 16:02:41
    平台运营人员根据专题模块属性不同，人工招商后，配置的商品

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.promotion.brand.theme.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.promotion.brand.theme.list"


class OpenDistributionCpsPromotionRecoTopicInfoRequest(RestApi):
    """
    获取推荐专题详细信息
    更新时间: 2021-12-28 11:14:05
    平台通过商品近期表现，多维度全方面评估后适宜不同属性模块的推荐商品

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.promotion.reco.topic.info&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.promotion.reco.topic.info"


class OpenDistributionCpsPromotionRecoTopicItemListRequest(RestApi):
    """
    获取推荐专题商品列表
    更新时间: 2021-12-28 11:16:24
    平台通过商品近期表现，多维度全方面评估后适宜不同属性模块的推荐商品

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.promotion.reco.topic.item.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.promotion.reco.topic.item.list"


class OpenDistributionCpsPromotionRecoTopicListRequest(RestApi):
    """
    获取推荐专题列表
    更新时间: 2021-12-28 11:16:48
    平台通过商品近期表现，多维度全方面评估后适宜不同属性模块的推荐商品

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.promotion.reco.topic.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.promotion.reco.topic.list"


class OpenDistributionCpsPromotionRecoTopicSellerListRequest(RestApi):
    """
    获取推荐专题商家列表
    更新时间: 2021-12-28 11:15:36
    平台通过商品近期表现，多维度全方面评估后适宜不同属性模块的推荐商品

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.promotion.reco.topic.seller.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.promotion.reco.topic.seller.list"


class OpenDistributionCpsPromotionThemeEntranceListRequest(RestApi):
    """
    获取站外分销专题列表
    更新时间: 2021-12-30 16:04:01
    平台运营人员根据专题模块属性不同，人工招商后，配置的商品

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.promotion.theme.entrance.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.promotion.theme.entrance.list"


class OpenDistributionCpsPromtionThemeItemListRequest(RestApi):
    """
    获取专题商品列表
    更新时间: 2021-12-30 16:05:51
    平台运营人员根据专题模块属性不同，人工招商后，配置的商品

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.cps.promtion.theme.item.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.cps.promtion.theme.item.list"


class OpenDistributionDistributionPlanAddPromoterRequest(RestApi):
    """
    分销计划新增达人佣金
    更新时间: 2021-12-30 16:07:38
    分销计划新增达人佣金

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.distribution.plan.add.promoter&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.distribution.plan.add.promoter"


class OpenDistributionDistributionPlanDeletePromoterRequest(RestApi):
    """
    删除达人
    更新时间: 2022-06-29 20:05:51
    删除达人

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.distribution.plan.delete.promoter&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.distribution.plan.delete.promoter"


class OpenDistributionInvestmentActivityAdjustactivitypromoterRequest(RestApi):
    """
    增减招商活动达人信息
    更新时间: 2023-08-03 15:28:04
    增减招商活动达人信息

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.investment.activity.adjustActivityPromoter&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.investment.activity.adjustActivityPromoter"


class OpenDistributionInvestmentActivityInvalidItemListRequest(RestApi):
    """
    招商活动失效商品列表
    更新时间: 2024-08-21 10:52:51
    招商活动失效商品列表

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.investment.activity.invalid.item.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.investment.activity.invalid.item.list"


class OpenDistributionInvestmentActivityItemDetailRequest(RestApi):
    """
    招商活动商品详情接口
    更新时间: 2025-04-02 15:42:15
    招商活动商品详情接口

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.investment.activity.item.detail&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.investment.activity.item.detail"


class OpenDistributionInvestmentActivityItemTokenCreateRequest(RestApi):
    """
    获取活动商品分享口令
    更新时间: 2024-07-25 19:22:10
    获取活动商品分享口令

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.investment.activity.item.token.create&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.investment.activity.item.token.create"


class OpenDistributionInvestmentActivityOpenCloseRequest(RestApi):
    """
    团长关闭招商活动
    更新时间: 2024-08-14 10:48:27
    团长关闭招商活动

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.investment.activity.open.close&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.investment.activity.open.close"


class OpenDistributionInvestmentActivityOpenCreateRequest(RestApi):
    """
    团长创建招商活动接口
    更新时间: 2024-10-15 17:38:19
    通过这个接口团长可以创建招商活动

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.investment.activity.open.create&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.investment.activity.open.create"


class OpenDistributionInvestmentActivityOpenDeleteRequest(RestApi):
    """
    团长删除招商活动
    更新时间: 2024-08-14 10:49:57
    团长删除招商活动

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.investment.activity.open.delete&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.investment.activity.open.delete"


class OpenDistributionInvestmentActivityOpenInfoRequest(RestApi):
    """
    获取活动详情
    更新时间: 2024-08-22 15:08:06
    获取活动详情

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.investment.activity.open.info&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.investment.activity.open.info"


class OpenDistributionInvestmentActivityOpenItemAuditRequest(RestApi):
    """
    团长审核活动报名商品
    更新时间: 2025-04-02 15:41:51
    团长审核活动报名商品

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.investment.activity.open.item.audit&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.investment.activity.open.item.audit"


class OpenDistributionInvestmentActivityOpenItemListRequest(RestApi):
    """
    团长招商活动已报名商品列表
    更新时间: 2024-10-15 17:39:12
    团长招商活动已报名商品列表

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.investment.activity.open.item.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.investment.activity.open.item.list"


class OpenDistributionInvestmentActivityOpenListRequest(RestApi):
    """
    团长查询招商活动列表
    更新时间: 2024-10-15 17:38:44
    团长查询招商活动列表

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.investment.activity.open.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.investment.activity.open.list"


class OpenDistributionInvestmentActivityOpenPromotionEffectRequest(RestApi):
    """
    招商活动推广效果
    更新时间: 2023-11-28 11:51:34
    招商活动推广效果

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.investment.activity.open.promotion.effect&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.investment.activity.open.promotion.effect"


class OpenDistributionInvestmentActivityQueryexclusivepromoterinfoRequest(RestApi):
    """
    查询专属活动达人信息
    更新时间: 2023-08-03 15:27:46
    查询专属活动达人信息

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.investment.activity.queryExclusivePromoterInfo&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.investment.activity.queryExclusivePromoterInfo"


class OpenDistributionInvestmentMyCreateActivityListRequest(RestApi):
    """
    查询我发起的招商活动
    更新时间: 2024-10-15 17:38:52
    (团长使用)查询我发起的招商活动

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.investment.my.create.activity.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.investment.my.create.activity.list"


class OpenDistributionItemSelectionAddUrlRequest(RestApi):
    """
    获取选品库页
    更新时间: 2022-06-30 11:52:57
    获取选品库页：生成的链接 需在登录状态下才能直接打开（或者生成二维码的方式，用户用快手app 扫描进去）

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.item.selection.add.url&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.item.selection.add.url"


class OpenDistributionItemShelfAddUrlRequest(RestApi):
    """
    获取新增商品页
    更新时间: 2022-06-29 22:26:02
    获取新增商品页

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.item.shelf.add.url&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.item.shelf.add.url"


class OpenDistributionKwaimoneyAuthorityCursorListRequest(RestApi):
    """
    站外推广达人列表
    更新时间: 2024-05-22 15:26:25
    获取有权限或者曾经有权限的站外推广达人列表(游标方式)

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.kwaimoney.authority.cursor.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.kwaimoney.authority.cursor.list"


class OpenDistributionKwaimoneyItemBatchCursorListRequest(RestApi):
    """
    批量获取站外推广需求商品信息
    更新时间: 2024-05-22 15:51:10
    批量获取站外推广需求商品信息

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.kwaimoney.item.batch.cursor.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.kwaimoney.item.batch.cursor.list"


class OpenDistributionKwaimoneyLiveItemListRequest(RestApi):
    """
    获取达人直播间小黄车上的商品列表
    更新时间: 2024-05-22 15:51:00
    获取达人直播间小黄车商品列表。
    1.达人必须设有有效的站外直播推广需求
    2.达人未直播则返回空列表
    3.同时返回分销商品和自建商品

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.kwaimoney.live.item.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.kwaimoney.live.item.list"


class OpenDistributionKwaimoneyPreheatWorkLinkRequest(RestApi):
    """
    获取推广需求的预热作品链接信息
    更新时间: 2022-01-04 11:28:28
    获取推广需求的预热作品链接信息

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.kwaimoney.preheat.work.link&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.kwaimoney.preheat.work.link"


class OpenDistributionKwaimoneyRequirementBatchCursorListRequest(RestApi):
    """
    批量达人的站外推广需求列表
    更新时间: 2024-05-22 15:47:54
    批量获取达人的站外推广需求列表，两种用法：
    1.queryBeginTime和queryEndTime置空，查询当前生效的需求。注意，在分页场景下每页请求对“当前”的定义不一定一致。
    2.若queryBeginTime为空，则查询queryEndTime时生效的需求。若queryBeginTime不为空，则查询在queryBeginTime到queryEndTime时间段内发生变动的需求。注意这种方式两次查询的数据可能有重复，需要对数据做幂等处理

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.kwaimoney.requirement.batch.cursor.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.kwaimoney.requirement.batch.cursor.list"


class OpenDistributionKwaimoneyRequirementCursorListRequest(RestApi):
    """
    单个达人的站外推广需求列表
    更新时间: 2024-05-22 15:31:18
    获取单个达人的站外推广需求列表，两种用法：
    1.queryBeginTime和queryEndTime置空，查询当前生效的需求。注意，在分页请求场景下每个分页请求对“当前”的定义不一定一致。
    2.若queryBeginTime为空，则查询queryEndTime时生效的需求。若queryBeginTime不为空，则查询在queryBeginTime到queryEndTime时间段内发生变动的需求。注意这种方式两次查询的数据可能有重复，需要对数据做幂等处理

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.kwaimoney.requirement.cursor.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.kwaimoney.requirement.cursor.list"


class OpenDistributionPidBindUrlRequest(RestApi):
    """
    获取绑定pid页
    更新时间: 2021-12-21 11:35:30
    获取绑定pid页

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.pid.bind.url&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.pid.bind.url"


class OpenDistributionPlanCommissionQueryRequest(RestApi):
    """
    查询计划佣金信息
    更新时间: 2024-09-18 17:08:59
    查询计划佣金信息

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.plan.commission.query&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.plan.commission.query"


class OpenDistributionPlanCreateRequest(RestApi):
    """
    创建分销计划
    更新时间: 2024-09-18 17:09:08
    创建分销计划

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.plan.create&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.plan.create"


class OpenDistributionPlanQueryRequest(RestApi):
    """
    查询商品计划信息
    更新时间: 2024-12-04 21:04:08
    查询商品计划信息

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.plan.query&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.plan.query"


class OpenDistributionPlanUpdateRequest(RestApi):
    """
    更新分销计划
    更新时间: 2025-02-25 16:29:20
    特殊说明：
    1.开启分销计划的前提是需要该计划处在关闭的状态下，并且商品处于上架状态才可以开启；
    2.普通计划、商品定向计划、店铺定向计划：开启状态下，下调佣金率次日0点生效，在23:50-24:00期间，不允许下调佣金率；
    3.如果接口调用不成功，都有具体的详细的业务报错信息。

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.plan.update&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.plan.update"


class OpenDistributionPromoteUpdateRequest(RestApi):
    """
    更新推广计划状态
    更新时间: 2024-04-22 14:32:53
    更新推广计划状态

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.promote.update&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.promote.update"


class OpenDistributionPublicCategoryListRequest(RestApi):
    """
    类目信息列表
    更新时间: 2023-12-26 16:07:27
    获取分销商品类目信息

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.public.category.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.public.category.list"


class OpenDistributionQuerySelectionItemDetailRequest(RestApi):
    """
    查询选品库商品详情
    更新时间: 2024-10-11 16:29:04
    查询选品库商品详情

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.query.selection.item.detail&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.query.selection.item.detail"


class OpenDistributionSecondActionApplyAgainInvestmentActivityRequest(RestApi):
    """
    商品取消合作后，再次报名(二级团长业务)
    更新时间: 2024-12-25 18:11:37
    商品取消合作后，再次报名，此接口只能以之前报名的费率重新报名，若要修改报名费率，请先使用修改商品报名服务费率接口修改，在使用该接口再次报名

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.second.action.apply.again.investment.activity&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.second.action.apply.again.investment.activity"


class OpenDistributionSecondActionApplyInvestmentActivityRequest(RestApi):
    """
    一级团长报名招商活动
    更新时间: 2024-01-11 13:59:26
    一级团长报名招商活动

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.second.action.apply.investment.activity&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.second.action.apply.investment.activity"


class OpenDistributionSecondActionCancelCooperationRequest(RestApi):
    """
    一级团长取消某商品的推广
    更新时间: 2024-08-14 10:50:51
    一级团长取消某商品的推广

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.second.action.cancel.cooperation&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.second.action.cancel.cooperation"


@deprecation.deprecated(details="已废弃")
class OpenDistributionSecondActionEditApplyInvestmentActivityRequest(RestApi):
    """
    [已废弃]修改商品报名服务费率
    更新时间: 2025-04-22 19:20:33
    修改商品报名服务费率，该接口用于一级团长报二级团长时，修改服务费率。

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.second.action.edit.apply.investment.activity&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.second.action.edit.apply.investment.activity"


class OpenDistributionSecondActionHandleCooperationRequest(RestApi):
    """
    二级团长审核一级团长对某商品取消推广
    更新时间: 2024-08-21 10:52:00
    二级团长审核一级团长对某商品取消推广的申请

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.second.action.handle.cooperation&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.second.action.handle.cooperation"


class OpenDistributionSecondAllowInvestmentActivityItemListRequest(RestApi):
    """
    一级团长查看能够报名招商活动的商品
    更新时间: 2024-05-29 19:23:38
    一级团长查看能够报名指定ID招商活动的商品

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.second.allow.investment.activity.item.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.second.allow.investment.activity.item.list"


class OpenDistributionSecondApplyInvestmentActivityItemListRequest(RestApi):
    """
    一级团长查看报名其它招商活动的商品
    更新时间: 2024-05-29 15:01:35
    一级团长查看自己报名其它招商活动的商品

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.second.apply.investment.activity.item.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.second.apply.investment.activity.item.list"


class OpenDistributionSecondApplyInvestmentActivityListRequest(RestApi):
    """
    一级团长查看自己报名的招商活动列表
    更新时间: 2024-05-29 15:02:17
    一级团长查看自己报名的招商活动列表

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.second.apply.investment.activity.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.second.apply.investment.activity.list"


class OpenDistributionSecondInvestmentActivityListRequest(RestApi):
    """
    一级团长可报名的招商活动列表
    更新时间: 2024-10-15 17:39:03
    (二级团长业务)一级团长可报名的招商活动列表

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.second.investment.activity.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.second.investment.activity.list"


class OpenDistributionSelectionOfflineRequest(RestApi):
    """
    达人货架商品下架
    更新时间: 2024-10-11 15:29:02
    达人货架商品下架，支持批量方式

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.selection.offline&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.selection.offline"


class OpenDistributionSelectionPickRequest(RestApi):
    """
    添加选品到货架
    更新时间: 2024-09-26 19:25:28
    添加选品到货架，支持批量方式

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.selection.pick&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.selection.pick"


class OpenDistributionSellerActivityApplyRequest(RestApi):
    """
    商家报名招商活动
    更新时间: 2024-06-18 10:26:00
    商家报名招商活动

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.seller.activity.apply&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.seller.activity.apply"


class OpenDistributionSellerActivityApplyCancelRequest(RestApi):
    """
    商家取消招商活动报名
    更新时间: 2024-08-21 10:51:08
    商家取消招商活动报名

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.seller.activity.apply.cancel&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.seller.activity.apply.cancel"


class OpenDistributionSellerActivityApplyListRequest(RestApi):
    """
    商家已报名的团长招商活动列表
    更新时间: 2024-06-17 14:30:03
    商家已报名的团长招商活动列表

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.seller.activity.apply.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.seller.activity.apply.list"


class OpenDistributionSellerActivityItemListRequest(RestApi):
    """
    商家已报名某活动商品列表
    更新时间: 2024-08-20 14:08:11
    商家已报名某活动商品列表

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.seller.activity.item.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.seller.activity.item.list"


class OpenDistributionSellerActivityOpenInfoRequest(RestApi):
    """
    商家查询活动信息
    更新时间: 2024-08-20 13:16:03
    商家查询活动信息

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.seller.activity.open.info&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.seller.activity.open.info"


class OpenDistributionSellerActivityOpenListRequest(RestApi):
    """
    商家获取团长招商活动列表
    更新时间: 2024-06-17 14:29:20
    商家获取团长招商活动列表

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.seller.activity.open.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.seller.activity.open.list"


class OpenDistributionSellerActivityPromotionEffectItemRequest(RestApi):
    """
    商家查询商品维度团长推广效果
    更新时间: 2023-08-24 14:34:54
    商家查询商品维度团长推广效果

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.seller.activity.promotion.effect.item&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.seller.activity.promotion.effect.item"


class OpenDistributionSellerActivityPromotionEffectSummaryRequest(RestApi):
    """
    卖家查看推广效果总览
    更新时间: 2023-08-24 14:34:38
    卖家查看推广效果总览

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.seller.activity.promotion.effect.summary&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.seller.activity.promotion.effect.summary"


class OpenDistributionInvestmentActivityQueryexclusivepromoterinfoRequest(RestApi):
    """
    查询专属活动达人信息
    更新时间: 2023-08-03 15:27:55
    查询专属活动达人信息

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.seller.activity.queryExclusivePromoterInfo&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.seller.activity.queryExclusivePromoterInfo"


class OpenDistributionSellerActivityUsableItemRequest(RestApi):
    """
    商家可报名商品列表
    更新时间: 2024-08-21 10:53:26
    商家可报名商品列表

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.seller.activity.usable.item&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.seller.activity.usable.item"


class OpenDistributionSellerSampleRuleSaveRequest(RestApi):
    """
    保存申样规则
    更新时间: 2024-07-30 11:08:24
    保存申样规则

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.distribution.seller.sample.rule.save&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.distribution.seller.sample.rule.save"


class OpenSellerOrderCpsDetailRequest(RestApi):
    """
    获取分销订单详情
    更新时间: 2024-10-17 19:38:44
    获取分销订单详情，未付款订单无法从该接口获取

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.seller.order.cps.detail&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.seller.order.cps.detail"


class OpenSellerOrderCpsListRequest(RestApi):
    """
    获取分销订单列表(游标方式)
    更新时间: 2024-10-17 19:38:34
    获取分销订单列表(游标方式)

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.seller.order.cps.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.seller.order.cps.list"
