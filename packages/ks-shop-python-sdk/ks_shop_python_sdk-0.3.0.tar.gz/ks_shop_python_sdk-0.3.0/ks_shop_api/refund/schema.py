# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional, List, Union


class OpenRefundCommentBasicListSchema(BaseModel):
    refundId: Optional[int] = Field(default=None, description="退款id")


class OpenRefundConfirmAndSendSchema(BaseModel):
    refundId: Optional[int] = Field(default=None, description="退款id")
    expressNo: Optional[str] = Field(default=None, description="快递单号")
    expressCode: Optional[int] = Field(default=None, description="快递公司编码")


class OpenRefundDirectRefundSchema(BaseModel):
    refundId: Optional[int] = Field(default=None, description="售后单id")
    refundVersion: Optional[int] = Field(default=None, description="售后单版本信息，值为为售后单的最近更新时间updateTime时间戳值")


class OpenRefundRejectSchema(BaseModel):
    refundId: Optional[int] = Field(default=None, description="退款单id")
    reasonCode: Optional[int] = Field(default=None, description="拒绝原因code，详情查看获取售后拒绝原因列表API open.refund.reject.reason")
    rejectDesc: Optional[str] = Field(default=None, description="拒绝相关描述，该字段是否必填由获取售后拒绝原因列表中返回的requiredRejectDesc字段决定")
    rejectImages: Optional[List[str]] = Field(default=None, description="拒绝相关图片，最多支持6张图片，该字段是否必填由获取售后拒绝原因列表中返回的requiredRejectImage字段决定")
    refundVersion: Optional[int] = Field(default=None, description="退款单版本，退款详情或退款列表中返回的更新时间(updateTime)字段")
    editHandlingWay: Optional[int] = Field(default=None, description="修改的退款方式")
    editReturnAddressId: Optional[int] = Field(default=None, description="修改的退货地址")


class OpenRefundRejectReasonSchema(BaseModel):
    refundId: Optional[int] = Field(default=None, description="退款单id")


class OpenRefundSubmitReturninfoSchema(BaseModel):
    refundId: Optional[int] = Field(default=None, description="退款单号")
    expressNo: Optional[str] = Field(default=None, description="快递单号")
    expressCode: Optional[int] = Field(default=None, description="快递公司编码")


class OpenSellerOrderRefundApproveSchema(BaseModel):
    refundId: Optional[int] = Field(default=None, description="退款单号")
    desc: Optional[str] = Field(default=None, description="退款说明（预计4月中旬下线）")
    refundAmount: Optional[Union[int, float]] = Field(default=None, description="退款金额 单位：分")
    status: Optional[int] = Field(default=None, description="退款单当前状态")
    negotiateStatus: Optional[int] = Field(default=None, description='协商状态，枚举： [1, "待商家处理"][2, "商家同意"][3, "商家驳回，等待买家修改"]')
    refundHandingWay: Optional[int] = Field(default=None, description='退款方式，枚举：[0, "未知"] [1, "退货退款"] [10,"仅退款"]')


class OpenSellerOrderRefundConfirmReceiptSchema(BaseModel):
    refundId: Optional[int] = Field(default=None, description="退款单号")
    status: Optional[int] = Field(default=None, description='当前退款单状态，枚举：仅支持退款单状态为 [22, "平台介入-已确认退货退款"] [30, "商品回寄信息待买家更新"] [40, "商品回寄信息待卖家确认"] 时，可调用确认收货接口')
    returnFreightHandlingAdvice: Optional[int] = Field(default=None, description='售后单详情的returnFreightInfo有值时填写，无值时不要填写。退货运费处理意见：1 同意，当选择同意时运费金额必填；2 拒绝，当选择拒绝时拒绝原因和图片必填')
    returnFreightAmount: Optional[Union[int, float]] = Field(default=None, description='当returnFreightHandlingAdvice(运费处理意见)为1(同意)时，运费金额必传且值为售后单详情出参returnFreightInfo. returnFreightAmount（商责退货运费金额）')
    returnFreightRejectDesc: Optional[str] = Field(default=None, description='当returnFreightHandlingAdvice(运费处理意见)为2(拒绝)时，拒绝原因描述必传，长度少于300')
    returnFreightRejectImages: Optional[List[str]] = Field(default=None, description='当returnFreightHandlingAdvice(运费处理意见)为2(拒绝)时，拒绝原因图片列表必传，最多6张')


class OpenSellerOrderRefundDetailSchema(BaseModel):
    refundId: Optional[int] = Field(default=None, description="售后单id")


class RefundPageOption(BaseModel):
    needExchange: Optional[bool] = Field(default=None, description="是否需要换货")


class OpenSellerOrderRefundPcursorListSchema(BaseModel):
    beginTime: Optional[int] = Field(default=None, description="订单生成的开始时间（单位毫秒），在当前时间的近90天内，不能大于90天，且小于截止时间")
    endTime: Optional[int] = Field(default=None, description="订单生成的截止时间（单位毫秒）在当前时间的近90天内，不能大于90天，且大于开始时间，且与开始时间的时间范围不大于1天 (与开始时间的时间范围建议做成随时可配置，该范围可能在活动期间随时变化，比如变成小时级或者分钟级)。")
    type: Optional[int] = Field(default=None, description="退款单请求类型，8 等待退款 9 全部退款订单")
    pageSize: Optional[int] = Field(default=None, description="每次请求数量，最多一页100条")
    currentPage: Optional[int] = Field(default=None, description="当前页码")
    sort: Optional[int] = Field(default=None, description="排序方式，1时间降序 2时间升序 ，默认降序")
    queryType: Optional[int] = Field(default=None, description="查找方式，1按创建时间查找 2按更新时间查找 ，默认创建时间")
    negotiateStatus: Optional[int] = Field(default=None, description='协商状态，1待商家处理 2 商家同意 3商家驳回，等待买家修改 默认返回所有数据')
    pcursor: Optional[str] = Field(default=None, description="游标内容，第一次传空串，之后传上一次的pcursor返回值，若返回“nomore”则标识到底")
    status: Optional[int] = Field(default=None, description='退款状态，枚举：[10, "买家已经申请退款，等待卖家同意"] [12, "卖家已拒绝，等待买家处理"] [20, "协商纠纷，等待平台处理"] [30, "卖家已经同意退款，等待买家退货"] [40, "买家已经退货，等待卖家确认收货"] [45, "卖家已经发货，等待买家确认收货"] [50, "卖家已经同意退款，等待系统执行退款"] [60, "退款成功"] [70, "退款关闭"]')
    option: Optional[RefundPageOption] = Field(default=None, description="选项")
    orderId: Optional[int] = Field(default=None, description="订单id，可根据订单id查询关联的所有售后单列表")


class OpenSellerOrderRefundReturngoodsApproveSchema(BaseModel):
    refundId: Optional[int] = Field(default=None, description="退款单号")
    refundAmount: Optional[Union[int, float]] = Field(default=None, description='退款金额 单位：分，仅用于校验和当前退款单的退款金额是否一致；当用于"商家同意换货"场景时，金额传入0')
    addressId: Optional[int] = Field(default=None, description="退货地址id，不传使用默认退货地址，可以通过获取商家地址列表API（open.address.seller.list）获取商家的退货地址")
