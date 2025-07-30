# -*- coding: utf-8 -*-
from ks_shop_api.base import RestApi
"""
工具 API
"""


class OpenToolWhiteipListAddRequest(RestApi):
    """
    新增应用ip白名单
    更新时间: 2022-12-02 14:48:05
    新增应用ip白名单

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.tool.whiteip.list.add&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.tool.whiteip.list.add"
