# -*- coding: utf-8 -*-
from ks_shop_api.base import RestApi
"""
短信 API
"""


class OpenPublicTemplateViewRequest(RestApi):
    """
    查询公共模板
    更新时间: 2023-07-21 18:14:18
    查询公共模板

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.public.template.view&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.public.template.view"


class OpenSmsBatchSendRequest(RestApi):
    """
    批量发送短信
    更新时间: 2023-11-01 19:40:23
    批量发送短信

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.sms.batch.send&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.sms.batch.send"


class OpenSmsCrowdSendRequest(RestApi):
    """
    发送短信给指定人群包
    更新时间: 2023-07-21 18:15:09
    通过人群包id给指定人群发送短信

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.sms.crowd.send&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.sms.crowd.send"


class OpenSmsExpressSendRequest(RestApi):
    """
    发送物流短信
    更新时间: 2023-11-01 19:43:56
    根据物流运单号发送物流短信，需要和平台对接联调

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.sms.express.send&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.sms.express.send"


class OpenSmsSendRequest(RestApi):
    """
    发送短信
    更新时间: 2023-11-01 19:51:09
    根据用户密文手机号发送短信

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.sms.send&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.sms.send"


class OpenSmsSendResultRequest(RestApi):
    """
    查询短信发送结果
    更新时间: 2023-11-03 11:45:13
    查询短信发送结果

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.sms.send.result&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.sms.send.result"


class OpenSmsSignApplyCreateRequest(RestApi):
    """
    申请短信签名
    更新时间: 2023-11-01 19:54:54
    短信签名申请接口，请注意短信签名名称必须要和快手小店店铺名称一致，短信签名规范参考文档 短信解决方案(https://open.kwaixiaodian.com/zone/new/solution/detail?pageSign=be565dfc5ca82ebb4683bc208f7929051642645445920#section-7)

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.sms.sign.apply.create&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.sms.sign.apply.create"


class OpenSmsSignDeleteRequest(RestApi):
    """
    删除短信签名
    更新时间: 2023-07-21 18:17:20
    删除短信签名

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.sms.sign.delete&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.sms.sign.delete"


class OpenSmsSignViewRequest(RestApi):
    """
    查询短信签名
    更新时间: 2023-07-21 18:17:47
    根据短信签名内容或ID查询短信签名详情和审核状态

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.sms.sign.view&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.sms.sign.view"


class OpenSmsTemplateApplyCreateRequest(RestApi):
    """
    申请短信模板
    更新时间: 2024-04-25 17:32:49
    申请短信模板，营销推广类短信必须以”拒收请回复R”结尾

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.sms.template.apply.create&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.sms.template.apply.create"


class OpenSmsTemplateDeleteRequest(RestApi):
    """
    删除短信模板
    更新时间: 2023-07-21 18:18:25
    删除短信模板

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.sms.template.delete&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.sms.template.delete"


class OpenSmsTemplateViewRequest(RestApi):
    """
    查询短信模板
    更新时间: 2023-07-21 18:18:49
    查询短信模板

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.sms.template.view&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.sms.template.view"
