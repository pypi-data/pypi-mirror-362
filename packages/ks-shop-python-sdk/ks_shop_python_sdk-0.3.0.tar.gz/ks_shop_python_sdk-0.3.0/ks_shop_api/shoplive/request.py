# -*- coding: utf-8 -*-
from ks_shop_api.base import RestApi
"""
电商直播 API
"""


class OpenLiveShopItemCheckOncarRequest(RestApi):
    """
    商品是否在小黄车
    更新时间: 2022-07-22 15:29:40
    判断商品当前是否在主播直播间挂车

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.live.shop.item.check.oncar&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.live.shop.item.check.oncar"


class OpenLiveShopSellerRealUvRequest(RestApi):
    """
    查询主播直播间的实时UV
    更新时间: 2022-07-22 15:29:16
    查询当前主播直播间的实时UV

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.live.shop.seller.real.uv&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.live.shop.seller.real.uv"


class OpenLieShopUserCarActionRequest(RestApi):
    """
    用户是否点击和加购小黄车
    更新时间: 2022-07-26 13:10:27
    判断用户是否在当前主播的直播间点击和加购了小黄车

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.live.shop.user.car.action&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.live.shop.user.car.action"


class OpenLiveShopWatchTimeMatchRequest(RestApi):
    """
    用户观看时长是否符合阈值
    更新时间: 2022-07-22 15:29:04
    判断用户在当前主播的直播间观看时长是否达到了传入的时长阈值，非实时获取，每20s获取一次时长，因此误差值在0s-20s之间

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.live.shop.watch.time.match&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.live.shop.watch.time.match"
