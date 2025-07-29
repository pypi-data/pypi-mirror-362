# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional, List, Union


class OpenDistributionCpsClipmcnOrderDetailSchema(BaseModel):
    distributorId: Optional[int] = Field(default=None, description="达人ID")
    clipUserId: Optional[int] = Field(default=None, description="剪手ID")
    oid: Optional[int] = Field(default=None, description="分销订单Id")


class OpenDistributionCpsClipmcnOrderListSchema(BaseModel):
    sortType: Optional[int] = Field(default=None, description="排序类型 [1:按指定查询类型降序] [2:按指定查询类型升序]")
    cpsOrderStatus: Optional[int] = Field(default=None, description="分销订单状态 [0:全部订单] [30:已付款] [50:已收货] [60:已结算] [80:已失效]")
    distributorId: Optional[int] = Field(default=None, description="达人ID [0:全部达人]")
    clipUserId: Optional[int] = Field(default=None, description="剪手ID")
    endTime: Optional[int] = Field(default=None, description="结束时间")
    beginTime: Optional[int] = Field(default=None, description="起始时间(单位: 毫秒， 起始时间为90天内，且订单时间跨度不超过7天)")
    pcursor: Optional[str] = Field(default=None, description='分销订单位点游标 (请求透传，"nomore"标识后续无数据)')
    queryType: Optional[int] = Field(default=None, description="查询类型 [1:按分销订单创建时间查询] [2:按分销订单更新时间查询][4:按订单实际创建时间查询]")
    pageSize: Optional[int] = Field(default=None, description="分页大小不超过100")


class OpenDistributionCpsDistributorOrderCommentListSchema(BaseModel):
    oid: Optional[List[int]] = Field(default=None, description="分销订单Id列表")
    sellerId: Optional[int] = Field(default=None, description="分销订单商家Id")


class OpenDistributionCpsDistributorOrderCursorListSchema(BaseModel):
    cpsOrderStatus: Optional[int] = Field(default=None, description="分销订单状态 [0:全部订单] [30:已付款] [50:已收货] [60:已结算] [80:已失效]")
    pageSize: Optional[int] = Field(default=None, description="分页大小不超过100")
    sortType: Optional[int] = Field(default=None, description="排序类型 [1:按指定查询类型降序] [2:按指定查询类型升序]")
    queryType: Optional[int] = Field(default=None, description="查询类型 [1:按订单下单时间查询] [2:按分销订单更新时间查询][3:按订单支付时间查询]，必传 （PS：订单需支付后才能从接口查到）")
    beginTime: Optional[int] = Field(default=None, description="起始时间(毫秒)，不能小于90天前，且需要小于结束时间")
    endTime: Optional[int] = Field(default=None, description="结束时间(毫秒)，且与开始时间的时间范围不大于7天 (与开始时间的时间范围建议做成随时可配置，该范围可能在活动期间随时变化，比如变成小时级或者分钟级)")
    pcursor: Optional[str] = Field(default=None, description='分销订单位点游标 (请求透传，"nomore"标识后续无数据)')


class OpenDistributionCpsKwaimoneyLinkCreateSchema(BaseModel):
    linkType: Optional[int] = Field(default=None, description="链接类型，100-直播间链接，101-商品链接")
    linkCarrierId: Optional[str] = Field(default=None, description="携带id（达人快手id或商品id）")
    comments: Optional[str] = Field(default=None, description="备注（透传字段，拉取订单接口返回）")
    cpsPid: Optional[str] = Field(default=None, description="快赚客推广位 cps pid")
    genPoster: Optional[bool] = Field(default=None, description="是否返回海报信息（默认值false，不返回海报信息）")
    customContent: Optional[str] = Field(default=None, description="自定义文案")
    activityId: Optional[int] = Field(default=None, description="一级活动id")
    secondActivityId: Optional[int] = Field(default=None, description="二级活动id")


class OpenDistributionCpsKwaimoneyLinkParseSchema(BaseModel):
    cpsLink: Optional[str] = Field(default=None, description="口令")


class OpenDistributionCpsKwaimoneyLinkTransferSchema(BaseModel):
    cpsLink: Optional[str] = Field(default=None, description="转链文案")
    kwaimoneyId: Optional[List[int]] = Field(default=None, description="快赚客ID集合 数量不超过20")


class OpenDistributionCpsKwaimoneyNewPromotionEffectDetailSchema(BaseModel):
    startTime: Optional[str] = Field(default=None, description="开始时间，格式yyyyMMdd，左闭右闭间")
    endTime: Optional[str] = Field(default=None, description="结束时间，格式yyyyMMdd，左闭右闭")
    offset: Optional[int] = Field(default=None, description="分页偏移量")
    limit: Optional[int] = Field(default=None, description="分页每页数量，阈值1000")
    orderField: Optional[int] = Field(default=None, description="排序字段：1-拉新量")
    orderType: Optional[int] = Field(default=None, description="排序规则：1-降序， 2-升序")
    cpsPid: Optional[str] = Field(default=None, description="快赚客推广位 cps pid")
    linkType: Optional[str] = Field(default=None, description="物料类型：100-直播间，101-商品")
    carrierId: Optional[int] = Field(default=None, description="主播id或商品id")
    buyerType: Optional[int] = Field(default=None, description="买家类型：0-平台新，1-电商新，2-平台回")


class OpenDistributionCpsKwaimoneyNewPromotionEffectTrendSchema(BaseModel):
    startTime: Optional[str] = Field(default=None, description="开始时间，格式yyyyMMdd，左闭右闭间")
    endTime: Optional[str] = Field(default=None, description="结束时间，格式yyyyMMdd，左闭右闭")
    cpsPid: Optional[str] = Field(default=None, description="快赚客推广位 cps pid")
    linkType: Optional[str] = Field(default=None, description="物料类型：100-直播间，101-商品")
    carrierId: Optional[int] = Field(default=None, description="主播id或商品id")
    buyerType: Optional[int] = Field(default=None, description="买家类型：0-平台新，1-电商新，2-平台回")


class OpenDistributionCpsKwaimoneyOrderDetailSchema(BaseModel):
    oid: Optional[List[int]] = Field(default=None, description="订单号列表，最多支持10个订单")


class OpenDistributionCpsKwaimoneyOrderListSchema(BaseModel):
    cpsOrderStatus: Optional[int] = Field(default=None, description="分销订单状态 [0:全部订单] [30:已付款] [50:已收货] [60:已结算] [80:已失效]")
    pageSize: Optional[int] = Field(default=None, description="页大小(最大限制为100)")
    sortType: Optional[int] = Field(default=None, description="排序类型 [1:按指定查询类型降序] [2:按指定查询类型升序]")
    queryType: Optional[int] = Field(default=None, description="查询类型 [1:按分销订单创建时间查询] [2:按分销订单更新时间查询]")
    beginTime: Optional[int] = Field(default=None, description="起始时间(毫秒)，不能小于90天前，且需要小于结束时间")
    endTime: Optional[int] = Field(default=None, description="结束时间(毫秒)，且与开始时间的时间范围不大于7天 (与开始时间的时间范围建议做成随时可配置，该范围可能在活动期间随时变化，比如变成小时级或者分钟级)")
    pcursor: Optional[str] = Field(default=None, description='分销订单位点游标 (请求透传，"nomore"标识后续无数据)')


class OpenDistributionCpsKwaimoneyPidCreateSchema(BaseModel):
    promotionBitName: Optional[str] = Field(default=None, description="推广位名称")


class OpenDistributionCpsKwaimoneyPidListSchema(BaseModel):
    page: Optional[int] = Field(default=None, description="页码")
    pageSize: Optional[int] = Field(default=None, description="页大小")


class OpenDistributionCpsKwaimoneyPidUpdateSchema(BaseModel):
    promotionBitName: Optional[str] = Field(default=None, description="推广位名称")
    cpsPid: Optional[str] = Field(default=None, description="快赚客推广位 cps pid")


class OpenDistributionCpsKwaimoneySelectionChannelListSchema(BaseModel):
    pass


class OpenDistributionCpsKwaimoneySelectionItemDetailSchema(BaseModel):
    itemId: Optional[List[int]] = Field(default=None, description="查询的商品ID，上限10个")


class RangeList(BaseModel):
    rangeId: Optional[str] = Field(default=None, description="筛选条件id：PRICE-商品价格，PROMOTION_RATE-佣金比率，THIRTY_DAYS_VOLUME-30天销量")
    rangeFrom: Optional[Union[int, float]] = Field(default=None, description="区间起始值")
    rangeTo: Optional[Union[int, float]] = Field(default=None, description="区间结束值")


class OpenDistributionCpsKwaimoneySelectionItemListSchema(BaseModel):
    rangeList: Optional[List[RangeList]] = Field(default=None, description="范围筛选列表")
    sortType: Optional[str] = Field(default=None, description="排序规则：DEFAULT_SORT-默认，RATE_ASC-佣金比率升序，RATE_DESC-佣金比率降序，PRICE_ASC-价格升序，PRICE_DESC-价格降序，VOLUME_ASC-30天销量升序，VOLUME_DESC-30天销量降序")
    pageIndex: Optional[str] = Field(default=None, description="分页游标，第一次请求不需传参，后续请求使用上次请求返回的值")
    channelId: Optional[List[int]] = Field(default=None, description="频道id列表")
    pageSize: Optional[int] = Field(default=None, description="分页大小，最大值为200")
    expressType: Optional[int] = Field(default=None, description="0或者不传：无筛选，1：不包邮，2:包邮")
    planType: Optional[int] = Field(default=None, description="分销计划类型。1-普通计划，2-商品定向4-店铺定向，5-专属计划，6-普通招商，7-专属招商")
    keyword: Optional[str] = Field(default=None, description="搜索关键词")
    itemLevel: Optional[str] = Field(default=None, description="商品分层等级。L1-新品上线,L2-达标分销商品,L3-优质好物,L4-行业爆款,L5-行业尖货")
    sellerId: Optional[int] = Field(default=None, description="卖家ID")
    itemTag: Optional[List[str]] = Field(default=None, description="商品标签")


class OpenDistributionCpsLeaderOrderCursorListSchema(BaseModel):
    sortType: Optional[int] = Field(default=None, description="排序类型 [1:按指定查询类型降序] [2:按指定查询类型升序]")
    queryType: Optional[int] = Field(default=None, description="查询类型 [1:按分销订单创建时间查询] [2:按分销订单更新时间查询][4:按订单实际创建时间查询] [6:按订单结算时间查询]")
    cpsOrderStatus: Optional[int] = Field(default=None, description="分销订单状态 [0:全部订单] [30:已付款] [50:已收货] [60:已结算] [80:已失效]")
    distributorId: Optional[int] = Field(default=None, description="达人ID [0:全部达人]")
    beginTime: Optional[int] = Field(default=None, description="起始时间(单位: 毫秒， 起始时间为90天内，且订单时间跨度不超过7天)")
    endTime: Optional[int] = Field(default=None, description="结束时间(单位: 毫秒)")
    pcursor: Optional[str] = Field(default=None, description='分销订单位点游标(下一次请求透传，返回"nomore"标识为结束)')
    pageize: Optional[int] = Field(default=None, description="分页大小不超过100")
    fundType: Optional[int] = Field(default=None, description="资金流转类型 [1:服务费收入订单] [2:服务费支出订单]")


class OpenDistributionCpsLeaderOrderDetailSchema(BaseModel):
    oid: Optional[int] = Field(default=None, description="订单ID")
    sellerId: Optional[int] = Field(default=None, description="商家ID")
    fundType: Optional[int] = Field(default=None, description="资金流转类型 [1:服务费收入订单] [2:服务费支出订单]")


class OpenDistributionCpsLinkCreateSchema(BaseModel):
    cpsPid: Optional[str] = Field(default=None, description="推广位pid")
    linkType: Optional[int] = Field(default=None, description="推广链接类型 100-直播间")
    linkCarrierId: Optional[str] = Field(default=None, description="推广链接载体ID 直播间则为推广主播用户快手ID")


class OpenDistributionCpsPidCreateSchema(BaseModel):
    promotionBitName: Optional[str] = Field(default=None, description="推广位名称")


class OpenDistributionCpsPidQuerySchema(BaseModel):
    page: Optional[int] = Field(default=None, description="页码")
    pageSize: Optional[int] = Field(default=None, description="页大小，最大50")


class OpenDistributionCpsPromoterOrderDetailSchema(BaseModel):
    oid: Optional[int] = Field(default=None, description="订单ID")
    sellerId: Optional[int] = Field(default=None, description="卖家ID")


class OpenDistributionCpsPromotionBrandThemeBrandListSchema(BaseModel):
    themeId: Optional[int] = Field(default=None, description="专题ID")
    pcursor: Optional[str] = Field(default=None, description="游标")
    subThemeId: Optional[int] = Field(default=None, description="子主题ID")


class OpenDistributionCpsPromotionBrandThemeItemListSchema(BaseModel):
    themeId: Optional[int] = Field(default=None, description="专题ID")
    orderBy: Optional[int] = Field(default=None, description="排序指标")
    pcursor: Optional[str] = Field(default=None, description="游标")
    subThemeId: Optional[int] = Field(default=None, description="子主题ID")
    searchSkat: Optional[int] = Field(default=None, description="优先展示（0：正常展示；1：优先展示SKA；2：优先展示非SKA）")
    brandId: Optional[int] = Field(default=None, description="品牌ID")


class OpenDistributionCpsPromotionBrandThemeListSchema(BaseModel):
    pass


class OpenDistributionCpsPromotionRecoTopicInfoSchema(BaseModel):
    topicId: Optional[int] = Field(default=None, description="专题ID")


class OpenDistributionCpsPromotionRecoTopicItemListSchema(BaseModel):
    themeId: Optional[int] = Field(default=None, description="子主题ID")
    pcursor: Optional[str] = Field(default=None, description="游标")
    topicId: Optional[int] = Field(default=None, description="推荐专题ID")
    channelId: Optional[int] = Field(default=None, description="频道ID")


class OpenDistributionCpsPromotionRecoTopicListSchema(BaseModel):
    pass


class OpenDistributionCpsPromotionRecoTopicSellerListSchema(BaseModel):
    themeId: Optional[int] = Field(default=None, description="子主题ID")
    pcursor: Optional[str] = Field(default=None, description="游标")
    topicId: Optional[int] = Field(default=None, description="主题ID")
    channelId: Optional[int] = Field(default=None, description="频道ID")


class OpenDistributionCpsPromotionThemeEntranceListSchema(BaseModel):
    pass


class OpenDistributionCpsPromtionThemeItemListSchema(BaseModel):
    themeId: Optional[int] = Field(default=None, description="专题ID")
    subThemeId: Optional[int] = Field(default=None, description="子主题ID")
    pcursor: Optional[str] = Field(default=None, description="游标")


class OpenDistributionDistributionPlanAddPromoterSchema(BaseModel):
    promoterId: Optional[List[int]] = Field(default=None, description="达人列表")
    commissionRate: Optional[int] = Field(default=None, description="佣金率（百分比：如20就是代表20%）")
    planId: Optional[int] = Field(default=None, description="计划ID")
    operator: Optional[str] = Field(default=None, description="操作人")


class OpenDistributionDistributionPlanDeletePromoterSchema(BaseModel):
    commissionId: Optional[List[int]] = Field(default=None, description="佣金ID")
    operator: Optional[str] = Field(default=None, description="操作人")


class OpenDistributionInvestmentActivityAdjustactivitypromoterSchema(BaseModel):
    promoterId: Optional[List[int]] = Field(default=None, description="达人ID列表")
    activityId: Optional[int] = Field(default=None, description="活动ID")
    operatorType: Optional[int] = Field(default=None, description="操作类型 1-增加；2-删减")


class OpenDistributionInvestmentActivityInvalidItemListSchema(BaseModel):
    offset: Optional[str] = Field(default=None, description="偏移量")
    itemId: Optional[int] = Field(default=None, description="商品id（可用于搜索）")
    activityId: Optional[int] = Field(default=None, description="活动id（可用于搜索）")
    limit: Optional[int] = Field(default=None, description="分页数（不超过20）")
    closeType: Optional[int] = Field(default=None, description="失效类型（0-全部，1-商品下架，2-商家取消合作，4-团长取消合作）")


class OpenDistributionInvestmentActivityItemDetailSchema(BaseModel):
    itemId: Optional[List[int]] = Field(default=None, description="商品idList")
    activityId: Optional[int] = Field(default=None, description="活动id")


class OpenDistributionInvestmentActivityItemTokenCreateSchema(BaseModel):
    itemId: Optional[int] = Field(default=None, description="商品ID")
    activityId: Optional[int] = Field(default=None, description="当前活动id")
    preActivityId: Optional[int] = Field(default=None, description="一级活动id（二级团商品必填）")


class OpenDistributionInvestmentActivityOpenCloseSchema(BaseModel):
    activityId: Optional[int] = Field(default=None, description="活动ID")


class CategoryCommissionRateDto(BaseModel):
    categoryId: Optional[int] = Field(default=None, description="类目ID(需要是叶子类目ID)")
    minCommissionRate: Optional[int] = Field(default=None, description="类目最低佣金率(千分位)")


class PromotionActivityMarketingRule(BaseModel):
    categoryCommissionRateList: Optional[List[CategoryCommissionRateDto]] = Field(default=None, description="类目佣金列表")
    minInvestmentPromotionRate: Optional[int] = Field(default=None, description="最低准入团长技术服务费率(千分位)")
    ruleType: Optional[int] = Field(default=None, description="0-叶子类目、2-二级类目、10-全部类目(类目佣金列表无需填写)")
    globalMinCommissionRate: Optional[int] = Field(default=None, description="设置批量佣金，ruleType选择全部类目时，该字段生效")


class InvestmentActivityRuleSet(BaseModel):
    promotionActivityMarketingRule: Optional[PromotionActivityMarketingRule] = Field(default=None, description="招商活动营销规则")


class OpenDistributionInvestmentActivityOpenCreateSchema(BaseModel):
    activityRuleSet: Optional[InvestmentActivityRuleSet] = Field(default=None, description="招商活动规则设置")
    activityEndTime: Optional[int] = Field(default=None, description="活动结束时间(毫秒)")
    activityType: Optional[int] = Field(default=None, description="活动类型（1：普通活动；2：专属活动；3：合作招商）")
    activityExclusiveUser: Optional[List[str]] = Field(default=None, description="专属达人ID列表（专属活动达人id和达人快手号任选进行填写）")
    activityBeginTime: Optional[int] = Field(default=None, description="活动开始时间(毫秒)")
    activityStatus: Optional[int] = Field(default=None, description="活动状态")
    activityTitle: Optional[str] = Field(default=None, description="活动标题")
    activityExclusiveUserKwaiId: Optional[List[str]] = Field(default=None, description="专属达人快手号列表（专属活动达人id和达人快手号任选进行填写）")
    preExclusiveActivitySignType: Optional[int] = Field(default=None, description="0,1-不允许其他团长报名专属活动，2-全部团长可报，3-指定团长可报")
    preActivityUser: Optional[List[int]] = Field(default=None, description="专属活动设置为指定团长可报名时，填写该字段上传团长ID。")
    mobilePhone: Optional[str] = Field(default=None, description="活动联系人手机号")
    wechat: Optional[str] = Field(default=None, description="活动联系人微信号")


class OpenDistributionInvestmentActivityOpenDeleteSchema(BaseModel):
    activityId: Optional[int] = Field(default=None, description="活动ID")


class OpenDistributionInvestmentActivityOpenInfoSchema(BaseModel):
    activityId: Optional[int] = Field(default=None, description="活动ID")


class ItemAuditDTO(BaseModel):
    itemId: Optional[int] = Field(default=None, description="商品ID")
    preActivityId: Optional[int] = Field(default=None, description="上一级活动id（二级团场景使用）")


class OpenDistributionInvestmentActivityOpenItemAuditSchema(BaseModel):
    itemAuditStatus: Optional[int] = Field(default=None, description="审核状态，2通过，3拒绝")
    itemId: Optional[List[int]] = Field(default=None, description="商品ID列表（已废弃）")
    activityId: Optional[int] = Field(default=None, description="活动ID")
    auditItem: Optional[List[ItemAuditDTO]] = Field(default=None, description="审核商品信息")


class OpenDistributionInvestmentActivityOpenItemListSchema(BaseModel):
    itemAuditStatus: Optional[int] = Field(default=None, description="商品审核状态")
    categoryId: Optional[int] = Field(default=None, description="类目ID")
    offset: Optional[int] = Field(default=None, description="分页偏移量（limit字段整数倍）")
    itemId: Optional[int] = Field(default=None, description="商品ID")
    activityId: Optional[int] = Field(default=None, description="活动ID")
    limit: Optional[int] = Field(default=None, description="每页数量")
    distributeSellerId: Optional[int] = Field(default=None, description="卖家ID")
    itemTitle: Optional[str] = Field(default=None, description="商品标题")


class OpenDistributionInvestmentActivityOpenListSchema(BaseModel):
    offset: Optional[int] = Field(default=None, description="查询偏移量（limit字段整数倍）")
    activityType: Optional[int] = Field(default=None, description="活动类型（1：普通活动；2：专属活动；3：合作招商）")
    limit: Optional[int] = Field(default=None, description="每页活动数量")
    activityId: Optional[int] = Field(default=None, description="活动ID")
    channelId: Optional[List[int]] = Field(default=None, description="频道ID")
    activityStatus: Optional[int] = Field(default=None, description="活动状态")
    activityTitle: Optional[str] = Field(default=None, description="活动标题")


class OpenDistributionInvestmentActivityOpenPromotionEffectSchema(BaseModel):
    pageCursor: Optional[int] = Field(default=None, description="分页游标")
    itemId: Optional[int] = Field(default=None, description="商品ID")
    activityId: Optional[int] = Field(default=None, description="活动ID")
    endTime: Optional[int] = Field(default=None, description="结束时间")
    itemTitle: Optional[str] = Field(default=None, description="商品标题")
    pageSize: Optional[int] = Field(default=None, description="每页大小")


class OpenDistributionInvestmentActivityQueryexclusivepromoterinfoSchema(BaseModel):
    offset: Optional[int] = Field(default=None, description="分页偏移量")
    activityId: Optional[int] = Field(default=None, description="活动ID")
    limit: Optional[int] = Field(default=None, description="分页限制")


class OpenDistributionInvestmentMyCreateActivityListSchema(BaseModel):
    offset: Optional[int] = Field(default=None, description="分页偏移量")
    limit: Optional[int] = Field(default=None, description="分页限制")
    activityType: Optional[int] = Field(default=None, description="活动类型（1：普通活动；2：专属活动；3：合作招商）")
    activityId: Optional[int] = Field(default=None, description="活动ID")
    activityStatus: Optional[int] = Field(default=None, description="活动状态 1-未发布，2-已发布，3-推广中，4-活动失效")
    activityTitle: Optional[str] = Field(default=None, description="活动标题")


class OpenDistributionItemSelectionAddUrlSchema(BaseModel):
    itemId: Optional[int] = Field(default=None, description="快手商品id")


class CategoryInfo(BaseModel):
    categoryId: Optional[int] = Field(default=None, description="类目ID")
    categoryName: Optional[str] = Field(default=None, description="类目名称")


class OpenDistributionItemShelfAddUrlSchema(BaseModel):
    itemKey: Optional[str] = Field(default=None, description="商品唯一标识（商品链接、口令、商品id等）")
    title: Optional[str] = Field(default=None, description="商品标题,若设置会使用设置值，若不设置取商品链接里头的信息")
    category: Optional[List[CategoryInfo]] = Field(default=None, description="商品对应快手商品类目信息，按照一级类目、二级类目...末级类目的顺序填写")


class OpenDistributionKwaimoneyAuthorityCursorListSchema(BaseModel):
    limit: Optional[int] = Field(default=None, description="单次请求上限")
    pcursor: Optional[str] = Field(default=None, description='位点游标(下一次请求透传，返回"nomore"标识为结束)')


class OpenDistributionKwaimoneyItemBatchCursorListSchema(BaseModel):
    id: Optional[List[int]] = Field(default=None, description="需求id列表")
    promoterId: Optional[int] = Field(default=None, description="达人ID")
    pcursor: Optional[str] = Field(default=None, description='分销订单位点游标(下一次请求透传，返回"nomore"标识为结束)')
    limit: Optional[int] = Field(default=None, description="单次请求限制条数")


class OpenDistributionKwaimoneyLiveItemListSchema(BaseModel):
    promoterId: Optional[int] = Field(default=None, description="达人ID")


class OpenDistributionKwaimoneyPreheatWorkLinkSchema(BaseModel):
    preheatWorkId: Optional[int] = Field(default=None, description="预热作品id")


class OpenDistributionKwaimoneyRequirementBatchCursorListSchema(BaseModel):
    promoterId: Optional[List[int]] = Field(default=None, description="达人id列表")
    queryEndTime: Optional[int] = Field(default=None, description="收集到指定时间的变动")
    limit: Optional[int] = Field(default=None, description="单次查询限额")
    pcursor: Optional[str] = Field(default=None, description='分销订单位点游标(下一次请求透传，返回"nomore"标识为结束)')
    queryBeginTime: Optional[int] = Field(default=None, description="上次同步任务的queryEndTime，如果是首次同步，置空。注意不是前个分页请求的queryEndTime")


class OpenDistributionKwaimoneyRequirementCursorListSchema(BaseModel):
    promoterId: Optional[int] = Field(default=None, description="达人ID")
    queryEndTime: Optional[int] = Field(default=None, description="收集到指定时间的变动")
    limit: Optional[int] = Field(default=None, description="单次查询限额")
    pcursor: Optional[str] = Field(default=None, description='分销订单位点游标(下一次请求透传，返回"nomore"标识为结束)')
    queryBeginTime: Optional[int] = Field(default=None, description="上次同步任务的queryEndTime，如果是首次同步，置空。注意不是前个分页请求的queryEndTime")


class OpenDistributionPidBindUrlSchema(BaseModel):
    pass


class OpenDistributionPlanCommissionQuerySchema(BaseModel):
    planId: Optional[int] = Field(default=None, description="计划ID")
    pcursor: Optional[str] = Field(default=None, description='查询游标，初始传空字符或"0"')


class ItemNormalPlanParam(BaseModel):
    itemIds: Optional[List[int]] = Field(default=None, description="商品ID列表")
    commissionRate: Optional[int] = Field(default=None, description="佣金比例（单位：百分比；范围：0-90）")


class ItemExclusivePlanParam(BaseModel):
    itemIds: Optional[List[int]] = Field(default=None, description="商品ID列表")
    promoterIds: Optional[List[int]] = Field(default=None, description="专属达人ID列表")
    commissionRate: Optional[int] = Field(default=None, description="佣金比例（单位：百分比；范围：0-90）")


class ItemOrientationPlanParam(BaseModel):
    itemIds: Optional[List[int]] = Field(default=None, description="定向商品列表")
    promoterIds: Optional[List[int]] = Field(default=None, description="定向达人ID列表")
    commissionRate: Optional[int] = Field(default=None, description="佣金比例（单位：百分比；范围：0-90）")


class OpenDistributionPlanCreateSchema(BaseModel):
    planCreateType: Optional[str] = Field(default=None, description="计划创建类型，ITEM_NORMAL-商品普通计划；ITEM_EXCLUSIVE-商品专属计划；ITEM_ORIENTATION-商品定向计划")
    normalPlanParam: Optional[ItemNormalPlanParam] = Field(default=None, description="创建商品普通计划参数，planCreateType为ITEM_NORMAL时必传")
    exclusivePlanParam: Optional[ItemExclusivePlanParam] = Field(default=None, description="创建商品专属计划参数，planCreateType为ITEM_EXCLUSIVE时必传")
    orientationPlanParam: Optional[ItemOrientationPlanParam] = Field(default=None, description="创建商品定向计划参数，planCreateType为ITEM_ORIENTATION时必传")


class OpenDistributionPlanQuerySchema(BaseModel):
    itemId: Optional[int] = Field(default=None, description="商品ID")


class UpdatePlanStatusParam(BaseModel):
    planId: Optional[int] = Field(default=None, description="计划ID")
    status: Optional[int] = Field(default=None, description="更新后的计划状态。1-开启；3-关闭")


class UpdateNormalCommissionParam(BaseModel):
    planId: Optional[int] = Field(default=None, description="计划ID")
    commissionRate: Optional[int] = Field(default=None, description="更新后的佣金比例（单位：百分比；范围：0-90）")


class UpdateOrientationCommissionParam(BaseModel):
    commissionId: Optional[int] = Field(default=None, description="佣金ID")
    commissionRate: Optional[int] = Field(default=None, description="更新后的佣金比例（单位：百分比；范围：0-90）")


class OpenDistributionPlanUpdateSchema(BaseModel):
    planId: Optional[int] = Field(default=None, description="计划ID")
    updateType: Optional[str] = Field(default=None, description="更新的信息类型，UPDATE_PLAN_STATUS-更新计划状态；UPDATE_NORMAL_COMMISSION-更新普通计划佣金；UPDATE_ORIENTATION_COMMISSION-更新计划定向/专属佣金")
    updatePlanStatusParam: Optional[UpdatePlanStatusParam] = Field(default=None, description="updateType为UPDATE_PLAN_STATUS时必传")
    updateNormalCommissionParam: Optional[UpdateNormalCommissionParam] = Field(default=None, description="updateType为UPDATE_NORMAL_COMMISSION时必传")
    updateOrientationCommissionParam: Optional[UpdateOrientationCommissionParam] = Field(default=None, description="updateType为UPDATE_ORIENTATION_COMMISSION时必传")


class OpenDistributionPromoteUpdateSchema(BaseModel):
    commissionId: Optional[List[int]] = Field(default=None, description="佣金ID")
    status: Optional[int] = Field(default=None, description="更改状态 1开启 3关闭")


class OpenDistributionPublicCategoryListSchema(BaseModel):
    pass


class OpenDistributionQuerySelectionItemDetailSchema(BaseModel):
    itemId: Optional[List[int]] = Field(default=None, description="	商品ID集合")


class OpenDistributionSecondActionApplyAgainInvestmentActivitySchema(BaseModel):
    investmentPromotionRate: Optional[int] = Field(default=None, description="服务费率，千分制")
    cooperationEndTime: Optional[int] = Field(default=None, description="商品合作结束时间")
    itemId: Optional[int] = Field(default=None, description="商品ID")
    cooperationStartTime: Optional[int] = Field(default=None, description="商品合作开始时间")
    activityId: Optional[int] = Field(default=None, description="报名的二级活动ID")
    preActivityId: Optional[int] = Field(default=None, description="该商品上一级活动ID")


class OpenDistributionSecondActionApplyInvestmentActivitySchema(BaseModel):
    itemId: Optional[List[int]] = Field(default=None, description="商品ID数组")
    activityId: Optional[int] = Field(default=None, description="报名的活动ID")
    preActivityId: Optional[int] = Field(default=None, description="该商品上一级活动ID")
    investmentPromotionRate: Optional[int] = Field(default=None, description="服务费率，千分制 100->10%，报名的服务费率不能低于当前报名活动的最低要求服务费率，不能大于该商品一级活动的服务费率")
    cooperationStartTime: Optional[int] = Field(default=None, description="合作开始时间，会根据当前时间、一级商品时间和二级活动时间动态调整")
    cooperationEndTime: Optional[int] = Field(default=None, description="合作结束时间，在一级商品时间范围内")


class OpenDistributionSecondActionCancelCooperationSchema(BaseModel):
    itemId: Optional[int] = Field(default=None, description="商品ID")
    activityId: Optional[int] = Field(default=None, description="报名的活动ID")
    preActivityId: Optional[int] = Field(default=None, description="该商品上一级活动ID")


class OpenDistributionSecondActionEditApplyInvestmentActivitySchema(BaseModel):
    itemId: Optional[int] = Field(default=None, description="商品ID")
    activityId: Optional[int] = Field(default=None, description="报名的二级活动ID")
    preActivityId: Optional[int] = Field(default=None, description="该商品上一级活动ID")
    itemCommissionRate: Optional[int] = Field(default=None, description="(扩展需要，目前无作用)佣金费率，千分制，100->10%")
    investmentPromotionRate: Optional[int] = Field(default=None, description="服务费率，千分制 100->10%，报名的服务费率不能低于当前报名活动的最低要求服务费率，不能大于该商品一级活动的服务费率")


class OpenDistributionSecondActionHandleCooperationSchema(BaseModel):
    itemId: Optional[int] = Field(default=None, description="商品ID")
    firstActivityUserId: Optional[int] = Field(default=None, description="提出申请的一级团长的ID")
    activityId: Optional[int] = Field(default=None, description="报名的二级活动ID")
    preActivityId: Optional[int] = Field(default=None, description="该商品上一级活动ID")
    itemAction: Optional[int] = Field(default=None, description="商品操作：在此接口中只能填4与5  4-不同意取消推广 5-同意取消推广")


class OpenDistributionSecondAllowInvestmentActivityItemListSchema(BaseModel):
    itemTitle: Optional[str] = Field(default=None, description="商品标题")
    itemId: Optional[int] = Field(default=None, description="商品ID")
    offset: Optional[int] = Field(default=None, description="分页偏移量")
    limit: Optional[int] = Field(default=None, description="分页每页数量")
    activityId: Optional[int] = Field(default=None, description="活动ID")
    itemAuditStatus: Optional[int] = Field(default=None, description="预留字段，忽略")
    categoryId: Optional[int] = Field(default=None, description="预留字段，忽略")
    queryScene: Optional[int] = Field(default=None, description="预留字段，忽略")
    itemIds: Optional[List[int]] = Field(default=None, description="预留字段，忽略")
    preActivityUserId: Optional[int] = Field(default=None, description="预留字段，忽略")


class OpenDistributionSecondApplyInvestmentActivityItemListSchema(BaseModel):
    itemTitle: Optional[str] = Field(default=None, description="预留字段，忽略")
    itemId: Optional[int] = Field(default=None, description="商品ID")
    itemAuditStatus: Optional[int] = Field(default=None, description="预留字段，忽略")
    categoryId: Optional[int] = Field(default=None, description="预留字段，忽略")
    activityUserId: Optional[int] = Field(default=None, description="预留字段，忽略")
    source: Optional[int] = Field(default=None, description="用户源 0——团长，1——商家，该接口为团长专用接口，强制填参数0，传其它参数返回结果无权限")
    queryScene: Optional[int] = Field(default=None, description="查询场景(扩展使用，无效参数)")
    itemIds: Optional[List[int]] = Field(default=None, description="预留字段，忽略")
    preActivityUserId: Optional[int] = Field(default=None, description="预留字段，忽略")
    offset: Optional[int] = Field(default=None, description="游标")
    limit: Optional[int] = Field(default=None, description="页大小")
    activityId: Optional[int] = Field(default=None, description="活动ID")


class OpenDistributionSecondApplyInvestmentActivityListSchema(BaseModel):
    activityType: Optional[int] = Field(default=None, description="活动类型 1-普通，2-专属")
    offset: Optional[int] = Field(default=None, description="分页偏移量")
    limit: Optional[int] = Field(default=None, description="分页大小")
    activityId: Optional[int] = Field(default=None, description="活动ID")


class OpenDistributionSecondInvestmentActivityListSchema(BaseModel):
    investmentSource: Optional[int] = Field(default=None, description="用户源 0-团长，1-商家。该接口为团长专用接口，强制填参数0，其它参数返回无权限提示。")
    activityTitle: Optional[str] = Field(default=None, description="预留字段，忽略")
    activityType: Optional[int] = Field(default=None, description="活动类型 1-普通活动，2-专属活动。")
    activityStatus: Optional[int] = Field(default=None, description="预留字段，忽略")
    channelId: Optional[List[int]] = Field(default=None, description="前台类目集合")
    offset: Optional[int] = Field(default=None, description="游标")
    limit: Optional[int] = Field(default=None, description="页大小")
    activityId: Optional[int] = Field(default=None, description="活动ID")
    createActivityUserId: Optional[int] = Field(default=None, description="创建该活动的团长ID")


class OpenDistributionSelectionOfflineSchema(BaseModel):
    itemId: Optional[List[int]] = Field(default=None, description="商品ID列表，最多50个")
    appName: Optional[str] = Field(default=None, description="开放平台appName，达人工作台的下架消息会使用此appName进行透出，请谨慎填写")


class ItemActivityDTO(BaseModel):
    itemId: Optional[int] = Field(default=None, description="商品ID")
    activityId: Optional[int] = Field(default=None, description="二级团活动id")
    preActivityId: Optional[int] = Field(default=None, description="一级团活动id")


class OpenDistributionSelectionPickSchema(BaseModel):
    itemIds: Optional[List[int]] = Field(default=None, description="商品ID列表")
    itemActivity: Optional[List[ItemActivityDTO]] = Field(default=None, description="团长活动信息")


class OpenDistributionSellerActivityApplySchema(BaseModel):
    investmentPromotionRate: Optional[int] = Field(default=None, description="团长服务费率(千分位)")
    itemId: Optional[List[int]] = Field(default=None, description="商品ID列表")
    activityId: Optional[int] = Field(default=None, description="活动ID")
    itemCommissionRate: Optional[int] = Field(default=None, description="商品佣金率(千分位)")
    contactUserOpenType: Optional[List[int]] = Field(default=None, description="[1]代表展示团长, [1,2]代表展示团长+达人，规则设置不能单独展示达人")
    baseOrderAmount: Optional[Union[int, float]] = Field(default=None, description="基础支付单量")
    cooperationStartTime: Optional[int] = Field(default=None, description="商品合作开始时间，默认取活动开始时间和当前时间的较大值")
    cooperationEndTime: Optional[int] = Field(default=None, description="商品合作结束时间")


class OpenDistributionSellerActivityApplyCancelSchema(BaseModel):
    itemId: Optional[int] = Field(default=None, description="商品ID")
    activityId: Optional[int] = Field(default=None, description="活动ID")


class OpenDistributionSellerActivityApplyListSchema(BaseModel):
    offset: Optional[int] = Field(default=None, description="分页偏移量（limit整数倍）")
    activityType: Optional[int] = Field(default=None, description="活动类型（1：普通活动；2：专属活动）")
    limit: Optional[int] = Field(default=None, description="每页活动数量")
    activityId: Optional[int] = Field(default=None, description="活动ID")


class OpenDistributionSellerActivityItemListSchema(BaseModel):
    itemAuditStatus: Optional[int] = Field(default=None, description="商品审核状态")
    categoryId: Optional[int] = Field(default=None, description="类目ID")
    offset: Optional[int] = Field(default=None, description="分页偏移量")
    itemId: Optional[int] = Field(default=None, description="商品ID")
    activityId: Optional[int] = Field(default=None, description="活动ID")
    limit: Optional[int] = Field(default=None, description="每页数量")
    itemTitle: Optional[str] = Field(default=None, description="商品标题")


class OpenDistributionSellerActivityOpenInfoSchema(BaseModel):
    activityId: Optional[int] = Field(default=None, description="活动ID")


class OpenDistributionSellerActivityOpenListSchema(BaseModel):
    offset: Optional[int] = Field(default=None, description="查询偏移量")
    activityType: Optional[int] = Field(default=None, description="活动类型")
    limit: Optional[int] = Field(default=None, description="每页活动数量")
    activityId: Optional[int] = Field(default=None, description="活动ID")
    channelId: Optional[List[int]] = Field(default=None, description="频道ID")
    activityTitle: Optional[str] = Field(default=None, description="活动标题")


class OpenDistributionSellerActivityPromotionEffectItemSchema(BaseModel):
    pageCursor: Optional[int] = Field(default=None, description="分页游标")
    itemId: Optional[int] = Field(default=None, description="商品ID")
    activityId: Optional[int] = Field(default=None, description="活动ID")
    endTime: Optional[int] = Field(default=None, description="结束时间")
    itemTitle: Optional[str] = Field(default=None, description="商品标题")
    pageSize: Optional[int] = Field(default=None, description="每页大小")


class OpenDistributionSellerActivityPromotionEffectSummarySchema(BaseModel):
    activityId: Optional[int] = Field(default=None, description="活动ID")
    endTime: Optional[int] = Field(default=None, description="结束时间")


class OpenDistributionInvestmentActivityQueryexclusivepromoterinfoSchema(BaseModel):
    offset: Optional[int] = Field(default=None, description="分页偏移量")
    activityId: Optional[int] = Field(default=None, description="活动ID")
    limit: Optional[int] = Field(default=None, description="分页限制")


class OpenDistributionSellerActivityUsableItemSchema(BaseModel):
    offset: Optional[int] = Field(default=None, description="分页偏移量（limit整数倍）")
    itemId: Optional[int] = Field(default=None, description="商品ID")
    activityId: Optional[int] = Field(default=None, description="活动ID")
    limit: Optional[int] = Field(default=None, description="每页活动数量")
    itemTitle: Optional[str] = Field(default=None, description="商品标题")


class QuotaConditionDto(BaseModel):
    quotaValue: Optional[str] = Field(default=None, description="指标值")
    quotaName: Optional[str] = Field(default=None, description="指标名称，总结算订单量：successOrderCount")


class ItemRuleDto(BaseModel):
    quotaCondition: Optional[List[QuotaConditionDto]] = Field(default=None, description="申样指标")
    applyType: Optional[int] = Field(default=None, description="申样类型 买样后返：2")


class SampleItemRuleDto(BaseModel):
    itemId: Optional[int] = Field(default=None, description="商品ID")
    itemRule: Optional[List[ItemRuleDto]] = Field(default=None, description="详细规则")


class OpenDistributionSellerSampleRuleSaveSchema(BaseModel):
    rule: Optional[List[SampleItemRuleDto]] = Field(default=None, description="申样规则")


class OpenSellerOrderCpsDetailSchema(BaseModel):
    distributorId: Optional[int] = Field(default=None, description="分销商ID")
    orderId: Optional[int] = Field(default=None, description="订单ID")


class OpenSellerOrderCpsListSchema(BaseModel):
    currentPage: Optional[int] = Field(default=None, description="当前页")
    pageSize: Optional[int] = Field(default=None, description="每页请求数量 最多一页80条")
    sort: Optional[int] = Field(default=None, description="1时间降序 2时间升序 默认降序")
    queryType: Optional[int] = Field(default=None, description="1按创建时间查找 2按更新时间查找 默认创建时间")
    type: Optional[int] = Field(default=None, description="订单状态，0未知 1 全部 2已付款 3 已收货 4 已结算5 已失效")
    pcursor: Optional[str] = Field(default=None, description="游标内容，第一次传空串，之后传上一次的pcursor返回值，若返回“nomore”则标识到底")
    distributorId: Optional[int] = Field(default=None, description="分销商ID")
    beginTime: Optional[int] = Field(default=None, description="订单生成时间的开始时间，单位毫秒，不能小于90天前，且需要小于结束时间")
    endTime: Optional[int] = Field(default=None, description="订单生成时间的截止时间，单位毫秒，不能小于90天前，且与开始时间的时间范围不大于1天 (与开始时间的时间范围建议做成随时可配置，该范围可能在活动期间随时变化，比如变成小时级或者分钟级)")
