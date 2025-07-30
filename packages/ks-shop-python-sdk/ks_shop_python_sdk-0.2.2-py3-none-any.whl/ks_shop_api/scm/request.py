# -*- coding: utf-8 -*-
from ks_shop_api.base import RestApi
"""
供应链 API
"""


class OpenScmInventoryAdjustRequest(RestApi):
    """
    调整货品库存
    更新时间: 2023-11-01 14:13:02
    货主调用该接口调整货品库存

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.scm.inventory.adjust&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.scm.inventory.adjust"


class OpenScmInventoryDetailRequest(RestApi):
    """
    查询货品库存
    更新时间: 2024-08-22 20:36:17
    货主调用该接口查询货品库存1111

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.scm.inventory.detail&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.scm.inventory.detail"


class OpenScmInventoryDisableRequest(RestApi):
    """
    库存禁用
    更新时间: 2022-09-20 17:41:48
    库存禁用

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.scm.inventory.disable&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.scm.inventory.disable"


class OpenScmInventoryUpdateRequest(RestApi):
    """
    库存全量更新接口
    更新时间: 2023-11-01 14:15:38
    库存全量更新接口

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.scm.inventory.update&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.scm.inventory.update"


class OpenScmQualitySingleBindRequest(RestApi):
    """
    绑定运单号
    更新时间: 2021-12-21 11:36:13
    绑定订单号和运单号

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.scm.quality.single.bind&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.scm.quality.single.bind"


class OpenScmWareAddRequest(RestApi):
    """
    添加货品
    更新时间: 2022-09-21 10:39:40
    添加货品

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.scm.ware.add&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.scm.ware.add"


class OpenScmWareDeleteRequest(RestApi):
    """
    禁用货品
    更新时间: 2022-09-21 10:39:09
    禁用货品

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.scm.ware.delete&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.scm.ware.delete"


class OpenScmWareInfoRequest(RestApi):
    """
    查询货品详情
    更新时间: 2023-11-01 14:16:41
    根据外部编码查询货品详情

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.scm.ware.info&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.scm.ware.info"


class OpenScmWareListRequest(RestApi):
    """
    查询货品列表
    更新时间: 2022-09-21 10:39:18
    查询货品列表

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.scm.ware.list&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.scm.ware.list"


class OpenScmWareUpdateRequest(RestApi):
    """
    更新货品
    更新时间: 2022-09-21 15:13:57
    根据外部编码更新货品

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.scm.ware.update&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.scm.ware.update"


class OpenScmWarehouseAddRequest(RestApi):
    """
    添加仓库
    更新时间: 2023-11-01 14:18:13
    添加仓库

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.scm.warehouse.add&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.scm.warehouse.add"


class OpenScmWarehouseDeleteRequest(RestApi):
    """
    禁用仓库
    更新时间: 2022-09-20 17:40:44
    禁用仓库

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.scm.warehouse.delete&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.scm.warehouse.delete"


class OpenScmWarehouseInfoRequest(RestApi):
    """
    查询仓库详情
    更新时间: 2022-09-20 17:41:33
    根据外部编码查询仓库详情

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.scm.warehouse.info&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.scm.warehouse.info"


class OpenScmWarehouseQueryRequest(RestApi):
    """
    查询仓库列表
    更新时间: 2022-09-20 17:41:24
    查询仓库列表

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.scm.warehouse.query&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.scm.warehouse.query"


class OpenScmWarehouseSalescopetemplateInfoRequest(RestApi):
    """
    查询仓库覆盖范围
    更新时间: 2022-09-20 17:41:17
    根据外部编码查询仓库覆盖范围

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.scm.warehouse.saleScopeTemplate.info&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.scm.warehouse.saleScopeTemplate.info"


class OpenScmWarehouseSalescopetemplateOperationRequest(RestApi):
    """
    设置仓库覆盖范围
    更新时间: 2023-11-01 14:19:38
    设置仓库覆盖范围

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.scm.warehouse.saleScopeTemplate.operation&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.scm.warehouse.saleScopeTemplate.operation"


class OpenScmWarehouseUpdateRequest(RestApi):
    """
    更新仓库
    更新时间: 2022-09-20 17:40:53
    根据仓库外部编码更新仓库

    https://open.kwaixiaodian.com/zone/new/docs/api?name=open.scm.warehouse.update&version=1
    """

    def __init__(self, app_key, secret, sign_secret):
        super().__init__(app_key, secret, sign_secret)

    def get_api_name(self):
        return "open.scm.warehouse.update"
