# -*- coding: utf-8 -*-
from ks_shop_api.base import RestApi
"""
短视频 API
"""


class OpenPhotoCountRequest(RestApi):
    """
    查询视频数量
    更新时间: 2024-10-14 22:28:47
    查询视频数量（商家子账号不能调用该接口）

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.photo.count&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.photo.count"


class OpenPhotoDeleteRequest(RestApi):
    """
    删除视频
    更新时间: 2024-10-14 22:29:19
    删除视频（商家子账号不能调用该接口）

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.photo.delete&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.photo.delete"


class OpenPhotoInfoRequest(RestApi):
    """
    查询单一视频详情
    更新时间: 2024-10-14 22:29:27
    查询单一视频详情（商家子账号不能调用该接口）

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.photo.info&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.photo.info"


class OpenPhotoListRequest(RestApi):
    """
    查询用户视频列表
    更新时间: 2024-10-14 22:30:03
    查询用户视频列表（商家子账号不能调用该接口）

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.photo.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.photo.list"


class OpenPhotoPublishRequest(RestApi):
    """
    发布视频
    更新时间: 2024-10-14 22:28:30
    发布视频（商家子账号不能调用该接口）
    1.流程为：使用创建视频API创建视频-上传视频-使用发布视频API发布视频，流程可查看短视频解决方案
    2.发布视频API详情示例可查看“短视频-发布视频示例“，注意Content-Type和body体参数

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.photo.publish&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.photo.publish"


class OpenPhotoStartUploadRequest(RestApi):
    """
    创建视频
    更新时间: 2024-10-14 22:27:53
    创建视频（商家子账号不能调用该接口）
    1.流程为：使用创建视频API创建视频-上传视频-使用发布视频API发布视频，流程可查看短视频解决方案
    2.创建视频API详情示例可查看“短视频-创建视频示例”

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.photo.start.upload&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.photo.start.upload"
