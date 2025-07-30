# -*- coding: utf-8 -*-
from ks_shop_api.base import RestApi
"""
客服 API
"""


class OpenCsLogisticsSessionCloseRequest(RestApi):
    """
    物流会话关闭
    更新时间: 2024-09-25 13:04:23
    物流会话关闭

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.cs.logistics.session.close&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.cs.logistics.session.close"


class OpenCsLogisticsSessionCreateCallbackRequest(RestApi):
    """
    物流会话创建回调
    更新时间: 2024-09-25 13:03:19
    物流会话创建回调

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.cs.logistics.session.create.callback&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.cs.logistics.session.create.callback"


class OpenCsLogisticsSessionMessagePullRequest(RestApi):
    """
    物流会话消息拉取
    更新时间: 2024-09-24 17:15:07
    物流会话消息拉取

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.cs.logistics.session.message.pull&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.cs.logistics.session.message.pull"


class OpenCsLogisticsSessionMessageSendRequest(RestApi):
    """
    物流会话消息发送
    更新时间: 2024-11-01 17:44:40
    物流会话消息发送

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.cs.logistics.session.message.send&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.cs.logistics.session.message.send"
