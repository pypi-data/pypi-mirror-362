# -*- coding: utf-8 -*-
from ks_shop_api.base import RestApi
"""
店铺 API
"""


class OpenScoreMasterGetRequest(RestApi):
    """
    获取带货口碑分信息
    更新时间: 2023-12-28 10:12:38
    获取带货口碑分信息，包括总分和多维度分

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.score.master.get&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.score.master.get"


class OpenScoreShopGetRequest(RestApi):
    """
    获取店铺体验分信息
    更新时间: 2023-12-28 10:12:15
    获取店铺体验分信息，包括总分和多维度分

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.score.shop.get&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.score.shop.get"


class OpenShopBrandPageGetRequest(RestApi):
    """
    获取店铺授权品牌列表
    更新时间: 2023-07-14 11:36:04
    1.获取用户对应的店铺已经授权的品牌资质，当返回状态为无效，表示该品牌资质已过期
    2.在店铺下找不到品牌，请确认该品牌资质是否已经审核通过，商家查询入口-品牌申报查询

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.shop.brand.page.get&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.shop.brand.page.get"


class OpenShopEnterpriseQualificaitonExistRequest(RestApi):
    """
    校验店铺资质
    更新时间: 2023-07-14 11:37:28
    1.用于校验店铺社会信用码是否存在并且和授权商家一致
    2.仅用于校验商家和社会信用码资质在平台是否经过验证，店铺经营状态请使用open.shop.info.get（获取店铺信息API）

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.shop.enterprise.qualificaiton.exist&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.shop.enterprise.qualificaiton.exist"


class OpenShopInfoGetRequest(RestApi):
    """
    获取店铺名称和类型
    更新时间: 2024-12-06 15:57:26
    获取当前用户的店铺信息，包括店铺名称和店铺类型

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.shop.info.get&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.shop.info.get"


class OpenShopPoiGetpoidetailbyouterpoiRequest(RestApi):
    """
    获取门店poi详情
    更新时间: 2023-07-21 18:01:19
    通过图商poi获取快手poi详情

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.shop.poi.getPoiDetailByOuterPoi&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.shop.poi.getPoiDetailByOuterPoi"
