# -*- coding: utf-8 -*-
from ks_shop_api.base import RestApi
"""
物流 API
"""


class OpenAddressDistrictListRequest(RestApi):
    """
    查询快手行政区划库
    更新时间: 2024-01-09 15:54:31
    快手目前使用的国家统计局的2021版本 直辖市名称一二级相同，如一级北京市，二级北京市。嘉峪关市 儋州市 中山市 东莞市下面的 三级和四级 名称一样， code也一样
    快手行政区划库旧版使用的是国家统计局2017版本，在此基础上添加了广东省深圳市光明区（440311）和四川省宜宾市叙州区（511504）。
    2017版为三级地址，2021版为四级地址，正向交易订单的收货地址已全量升级为四级地址，入参请使用2021版本

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.address.district.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.address.district.list"


class OpenAddressSellerCreateRequest(RestApi):
    """
    新增商家地址
    更新时间: 2024-01-09 16:20:29
    1.商家的发货地址和退货地址创建时若设为默认地址，则其它同类型地址都被设为非默认
    2.商家的发货地址和退货地址最多可以各创建50个
    3.若商家的发货地址或退货地址需要超过50个，请在支持中心-提交工单
    4. 目前地址录入行政区划，已开启校验，行政区划 只接收快手行政区地址API 2021版本四级地址信息

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.address.seller.create&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.address.seller.create"


class OpenAddressSellerDeleteRequest(RestApi):
    """
    删除商家地址
    更新时间: 2023-10-30 11:02:39
    删除商家地址，不允许删除默认地址

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.address.seller.delete&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.address.seller.delete"


class OpenAddressSellerGetRequest(RestApi):
    """
    获取商家地址详情
    更新时间: 2023-07-21 16:48:03
    通过地址ID获取商家地址详情

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.address.seller.get&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.address.seller.get"


class OpenAddressSellerListRequest(RestApi):
    """
    查询商家地址列表
    更新时间: 2023-06-07 11:15:26
    查询商家地址列表

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.address.seller.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.address.seller.list"


class OpenAddressSellerUpdateRequest(RestApi):
    """
    更新商家地址
    更新时间: 2024-07-08 11:29:55
    根据地址id更新商家地址管理里的地址信息，若更新时设为默认地址，则将其它地址都设为非默认；更新时不允许将默认地址设为非默认地址。

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.address.seller.update&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.address.seller.update"


class OpenLogisticsExpressTemplateAddRequest(RestApi):
    """
    新增运费模板
    更新时间: 2024-07-11 14:29:44
    新增运费模板，非偏远地区必须包邮，偏远地区建议包邮，使用详见《【运费模板】使用教程》

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.logistics.express.template.add&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.logistics.express.template.add"


class OpenLogisticsExpressTemplateDetailRequest(RestApi):
    """
    查询运费模板详情
    更新时间: 2024-07-16 11:41:03
    根据运费模板id查询运费模板，结合快手行政区划库接口open.address.district.list进行查询

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.logistics.express.template.detail&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.logistics.express.template.detail"


class OpenLogisticsExpressTemplateListRequest(RestApi):
    """
    批量查询运费模板
    更新时间: 2024-10-16 16:51:32
    根据偏移量、查询结果数、是否被使用 批量查询运费模板

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.logistics.express.template.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.logistics.express.template.list"


class OpenLogisticsExpressTemplateSaleLimitRequest(RestApi):
    """
    查询商家所有运费模板限售信息
    更新时间: 2025-06-05 15:50:34
    查询商家所有运费模板限售信息

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.logistics.express.template.sale.limit&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.logistics.express.template.sale.limit"


class OpenLogisticsExpressTemplateSaleLimitRemoveRequest(RestApi):
    """
    一键解除全部模板限售
    更新时间: 2025-06-05 15:49:56
    一键解除全部模板限售

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.logistics.express.template.sale.limit.remove&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.logistics.express.template.sale.limit.remove"


class OpenLogisticsExpressTemplateUpdateRequest(RestApi):
    """
    更新运费模板
    更新时间: 2024-07-11 14:29:35
    更新运费模板，非偏远地区必须包邮，偏远地区建议包邮，使用详见《【运费模板】使用教程》

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.logistics.express.template.update&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.logistics.express.template.update"


class OpenLogisticsTroubleNetSitePageQueryRequest(RestApi):
    """
    差网点分页查询
    更新时间: 2024-11-11 16:36:52
    分页查询差网点管控信息

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.logistics.trouble.net.site.page.query&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.logistics.trouble.net.site.page.query"
