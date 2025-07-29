# -*- coding: utf-8 -*-
from ks_shop_api.base import RestApi
"""
售后退款 API
"""


class OpenRefundCommentBasicListRequest(RestApi):
    """
    获取售后协商历史
    更新时间: 2023-09-19 11:15:13
    获取售后协商历史信息，包含节点、角色和时间

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.refund.comment.basic.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.refund.comment.basic.list"


class OpenRefundConfirmAndSendRequest(RestApi):
    """
    商家确认收货并发货
    更新时间: 2023-08-10 17:29:43
    换货场景下，商家确认收到了买家寄回的旧商品，并给买家寄送了换货的新商品，商家确认收货并发换货

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.refund.confirm.and.send&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.refund.confirm.and.send"


class OpenRefundDirectRefundRequest(RestApi):
    """
    商家直接退款给买家
    更新时间: 2023-07-14 14:16:51
    仅适用于换货场景，请谨慎操作
    1.换货单在待处理状态、商家同意换货后、商家拒绝换货后、买家申请平台介入后，都可以直接退款给买家
    2.换货单在商家确认收货并发货后、完整的换货流程结束后，不可以直接退款给买家

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.refund.direct.refund&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.refund.direct.refund"


class OpenRefundRejectRequest(RestApi):
    """
    商家拒绝收货退款
    更新时间: 2023-10-31 15:14:32
    1.商家拒绝仅退款申请、拒绝退货退款申请、拒绝换货申请
    2.商家拒绝收货
    3.商家修改售后单类型（退货退款——>仅退款，仅退款——>退货退款，换货——>退货退款）

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.refund.reject&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.refund.reject"


class OpenRefundRejectReasonRequest(RestApi):
    """
    获取售后拒绝原因列表
    更新时间: 2023-10-31 15:20:53
    根据售后单ID获取仅退款和退货退款拒绝原因列表

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.refund.reject.reason&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.refund.reject.reason"


class OpenRefundSubmitReturninfoRequest(RestApi):
    """
    商家代客填写退货单号
    更新时间: 2023-10-31 15:21:37
    商家代客填写退货单号

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.refund.submit.returnInfo&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.refund.submit.returnInfo"


class OpenSellerOrderRefundApproveRequest(RestApi):
    """
    商家同意退款
    更新时间: 2023-11-01 14:45:53
    1.售后单类型为仅退款时,调用该API完成退款操作
    2.售后单类型为退货退款时,使用open.seller.order.refund.returngoods.approve(商家同意退货API)完成同意退货操作

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.seller.order.refund.approve&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.seller.order.refund.approve"


class OpenSellerOrderRefundConfirmReceiptRequest(RestApi):
    """
    商家确认收货
    更新时间: 2024-05-11 14:43:30
    仅适用于退货退款售后单
    1.仅支持售后单类型为退货退款调用，此API会确认收货并直接给买家退款
    2.仅支持在退款单状态为“22平台介入-已确认退货退款”“30商品回寄信息待买家更新”“40商品回寄信息待卖家确认”时调用此API
    3.当售后单详情的returnFreightInfo没有值时，此API只需传refundId，returnFreight退货运费相关字段都不要传，否则会报错
    4.当售后单详情的returnFreightInfo有值时，且需要同意退货运费时，此API需传refundId、returnFreightHandlingAdvice、returnFreightAmount，若退货运费金额未传或值不一致会报错
    5.当售后单详情的returnFreightInfo有值时，且需要拒绝退货运费时，此API需传refundId、returnFreightHandlingAdvice、returnFreightRejectDesc、returnFreightRejectImages

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.seller.order.refund.confirm.receipt&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.seller.order.refund.confirm.receipt"


class OpenSellerOrderRefundDetailRequest(RestApi):
    """
    获取售后单详情
    更新时间: 2024-10-27 17:45:05
    根据售后单id查询售后单详情，handlingway为售后方式，status为售后状态

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.seller.order.refund.detail&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.seller.order.refund.detail"


class OpenSellerOrderRefundPcursorListRequest(RestApi):
    """
    获取售后单列表
    更新时间: 2024-04-22 16:28:28
    查询商家售后单列表(游标方式)，可根据订单id查询关联的全量售后单列表，handlingway为售后方式，status为售后状态

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.seller.order.refund.pcursor.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.seller.order.refund.pcursor.list"


class OpenSellerOrderRefundReturngoodsApproveRequest(RestApi):
    """
    商家同意退货
    更新时间: 2023-11-01 16:47:23
    1.商家同意退货
    2.商家同意换货

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.seller.order.refund.returngoods.approve&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.seller.order.refund.returngoods.approve"
