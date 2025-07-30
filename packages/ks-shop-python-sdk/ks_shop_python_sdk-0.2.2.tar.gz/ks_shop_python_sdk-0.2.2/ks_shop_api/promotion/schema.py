# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional, List, Union


class OpenPromotionCouponCreateSchema(BaseModel):
    validStartTime: Optional[int] = Field(default=None, description="使用开始时间，必须以00:00:00开始的，validityType为1的时候必传")
    outerUniqueKey: Optional[str] = Field(default=None, description="outer_unique_key 调用方唯一key ，字符长度<=60 ，outer_source_type 和 outer_unique_key 结合进行幂等处理")
    itemIds: Optional[List[int]] = Field(default=None, description="couponTargetType为0是必传")
    fixedValidityTime: Optional[int] = Field(default=None, description="固定有效期数值，validityType为2的时候必传")
    receiveChannel: Optional[str] = Field(default=None, description="领取渠道。多个渠道用逗号隔开。1-商详，74-客服发券，40-全部推广渠道，76-活动渠道")
    reduceAmount: Optional[Union[int, float]] = Field(default=None, description="优惠券金额")
    receiveStartTime: Optional[int] = Field(default=None, description="领取开始时间，必须以00:00:00开始的")
    threshold: Optional[Union[int, float]] = Field(default=None, description="优惠券门槛")
    couponTargetType: Optional[int] = Field(default=None, description="0-商品 1-店铺 2-类目 3-全平台通用")
    extInfo: Optional[str] = Field(default=None, description='扩展信息。如果是新粉券，{"focusSecondTime":1212}，value是秒')
    validityType: Optional[int] = Field(default=None, description="优惠券使用有效期类型 1-时间段(start-end) 2-固定时间fixedTime")
    validEndTime: Optional[int] = Field(default=None, description="	使用结束时间，必须以23:59:59结尾，validityType为1的时候必传")
    receiveEndTime: Optional[int] = Field(default=None, description="领取结束时间，必须以23:59:59结尾")
    name: Optional[str] = Field(default=None, description="优惠券名称")
    totalStock: Optional[int] = Field(default=None, description="总库存")
    receivePerLimit: Optional[int] = Field(default=None, description="每人限领")
    couponFrontType: Optional[int] = Field(default=None, description="券类型。10-新粉券，11-粉丝券")


class OpenPromotionCouponDeleteSchema(BaseModel):
    couponId: Optional[int] = Field(default=None, description="优惠券ID")


class OpenPromotionCouponOverSchema(BaseModel):
    couponId: Optional[int] = Field(default=None, description="优惠券ID")


class OpenPromotionCouponPageListSchema(BaseModel):
    couponTargetType: Optional[int] = Field(default=None, description="0-商品券，1-店铺券，15-主播红包")
    pageNo: Optional[int] = Field(default=None, description="页号，从1开始")
    sellerCouponStatus: Optional[int] = Field(default=None, description="0-全部。1-未开始，2-可领取，3-已结束")
    pageSize: Optional[int] = Field(default=None, description="页大小")


class OpenPromotionCouponQuerySchema(BaseModel):
    couponId: Optional[List[int]] = Field(default=None, description="优惠券id集合")


class OpenPromotionCouponSendSchema(BaseModel):
    couponConfigId: Optional[int] = Field(default=None, description="券配置id")
    outerId: Optional[str] = Field(default=None, description="外部幂等id")
    receiveChannel: Optional[int] = Field(default=None, description="领取渠道")
    userOpenId: Optional[str] = Field(default=None, description="c端用户id")


class OpenPromotionCouponStatisticSchema(BaseModel):
    couponId: Optional[int] = Field(default=None, description="优惠券ID")
    businessLine: Optional[int] = Field(default=None, description="业务线，1-快手小店")


class OpenPromotionCouponStockAddSchema(BaseModel):
    couponId: Optional[int] = Field(default=None, description="优惠券ID")
    incrementNum: Optional[int] = Field(default=None, description="增加、减少数量")


class TagCondition(BaseModel):
    startTime: Optional[str] = Field(default=None, description="开始时间")
    tagName: Optional[str] = Field(default=None, description="人群包名称")
    conditionOperator: Optional[str] = Field(default=None, description="条件操作符")
    endTime: Optional[str] = Field(default=None, description="结束时间")
    value: Optional[List[str]] = Field(default=None, description="标签值数组")


class OpenPromotionCrowdCreateSchema(BaseModel):
    crowdDesc: Optional[str] = Field(default=None, description="人群包描述")
    extJson: Optional[str] = Field(default=None, description="附加参数")
    crowdName: Optional[str] = Field(default=None, description="人群包名称")
    tagCondition: Optional[List[TagCondition]] = Field(default=None, description="标签信息")


class OpenPromotionCrowdDetailSchema(BaseModel):
    crowdId: Optional[int] = Field(default=None, description="人群包ID")


class OpenPromotionCrowdEditSchema(BaseModel):
    crowdDesc: Optional[str] = Field(default=None, description="人群包描述")
    extJson: Optional[str] = Field(default=None, description="附加参数")
    crowdName: Optional[str] = Field(default=None, description="人群包名称")
    tagCondition: Optional[List[TagCondition]] = Field(default=None, description="标签信息")
    crowdId: Optional[int] = Field(default=None, description="人群包ID")


class OpenPromotionCrowdPredictSchema(BaseModel):
    extJson: Optional[str] = Field(default=None, description="附加参数")
    tagCondition: Optional[List[TagCondition]] = Field(default=None, description="标签信息")


class OpenPromotionSellerStatisticSchema(BaseModel):
    startTime: Optional[int] = Field(default=None, description="开始时间，毫秒，传入的时间范围需小于1天，或者时间范围为7天、1个月")
    endTime: Optional[int] = Field(default=None, description="结束时间，毫秒，传入的时间范围需小于1天，或者时间范围为7天、1个月")
    businessLine: Optional[int] = Field(default=None, description="业务线，传1")
    couponTarget: Optional[int] = Field(default=None, description="0-商品，1-店铺，9-全部")


class OpenPromotionShopNewbieCreateSchema(BaseModel):
    couponTargetType: Optional[int] = Field(default=None, description="券的作用对象类型，0-商品，1-店铺")
    itemIds: Optional[List[int]] = Field(default=None, description="couponTargetType是0时，指定的商品id")
    couponPrice: Optional[Union[int, float]] = Field(default=None, description="券面额，分")
    couponEnd: Optional[int] = Field(default=None, description="券结束时间，毫秒，要依23:59:59结尾的时间换成毫秒数")
    couponFrontType: Optional[int] = Field(default=None, description="券类型，店铺新人传1")
    couponBase: Optional[int] = Field(default=None, description="券门槛，分")
    status: Optional[int] = Field(default=None, description="券状态，传 0")
