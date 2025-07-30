# -*- coding: utf-8 -*-
from ks_shop_api.base import RestApi
"""
评价 API
"""


class OpenCommentAddRequest(RestApi):
    """
    回复评价
    更新时间: 2023-10-30 11:13:12
    商家回复订单的评价，当前支持文字回复
    1.商家在买家评价后30天内允许回复评价，请注意追加评价前注意时间
    2.商家不允许修改评价
    3.商家回复评价仅支持回复首次的评价
    4.“确认收货“且未评价的订单也支持评价
    5.买家评价后的180天允许买家追加评价

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.comment.add&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.comment.add"


class OpenCommentListGetRequest(RestApi):
    """
    查询评价列表
    更新时间: 2025-04-15 15:21:28
    查询当前商家的评价列表

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.comment.list.get&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.comment.list.get"


class OpenSubcommentListGetRequest(RestApi):
    """
    查询自评价
    更新时间: 2023-07-21 18:04:59
    根据主评价查询子评价详情

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.subcomment.list.get&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.subcomment.list.get"
