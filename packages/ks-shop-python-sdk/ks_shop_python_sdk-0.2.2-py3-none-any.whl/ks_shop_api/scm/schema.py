# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional, List, Union


class OpenScmInventoryAdjustSchema(BaseModel):
    wareOutCode: Optional[str] = Field(default=None, description="货品外部编码")
    idempotentId: Optional[str] = Field(default=None, description="幂等键")
    warehouseOutCode: Optional[str] = Field(default=None, description="外部仓库编码")
    operationType: Optional[str] = Field(default=None, description="调整方向（增加/减少）")
    adjustQuantity: Optional[Union[int, float]] = Field(default=None, description="调整数量。如果库存不足，就回返回实际变更的值")


class OpenScmInventoryDetailSchema(BaseModel):
    wareOutCode: Optional[str] = Field(default=None, description="外部货品编码")


class OpenScmInventoryDisableSchema(BaseModel):
    wareOutCode: Optional[str] = Field(default=None, description="外部货品编码")
    warehouseOutCode: Optional[str] = Field(default=None, description="外部仓库编码")


class OpenScmInventoryUpdateSchema(BaseModel):
    quantity: Optional[Union[int, float]] = Field(default=None, description="库存数量。大于等于0")
    wareOutCode: Optional[str] = Field(default=None, description="外部货品编码")
    warehouseOutCode: Optional[str] = Field(default=None, description="外部仓库编码")


class OpenScmQualitySingleBindSchema(BaseModel):
    orderId: Optional[str] = Field(default=None, description="订单ID")
    expressNo: Optional[str] = Field(default=None, description="出库运单号（物流单号）")
    expressCode: Optional[str] = Field(default=None, description="物流公司编码 ZTO")


class OpenScmWareAddSchema(BaseModel):
    wareVolume: Optional[Union[int, float]] = Field(default=None, description="货品体积，单位立方厘米，不超过10位数")
    wareName: Optional[str] = Field(default=None, description="货品名称")
    wareHeight: Optional[Union[int, float]] = Field(default=None, description="货品高度，单位厘米，不超过6位数")
    wareWidth: Optional[Union[int, float]] = Field(default=None, description="货品宽度，单位厘米，不超过6位数")
    wareOutCode: Optional[str] = Field(default=None, description="外部编码")
    ownerSourceName: Optional[str] = Field(default=None, description="源头供货商名称")
    wareLength: Optional[Union[int, float]] = Field(default=None, description="货品长度，单位厘米，不超过6位数")
    ownerSourceTypeEnum: Optional[str] = Field(default=None, description="源头供货商类型，枚举值：1、工厂采购 MANUFACTORY_PURCHASE，2、品牌直供BRAND_DIRECT_SUPPLY，3、品牌经销BRAND_DEAL")
    barcode: Optional[str] = Field(default=None, description="条形码")
    wareWeight: Optional[Union[int, float]] = Field(default=None, description="货品重量，单位克，不超过10位数")


class OpenScmWareDeleteSchema(BaseModel):
    wareOutCode: Optional[str] = Field(default=None, description="外部货品编码")


class OpenScmWareInfoSchema(BaseModel):
    wareOutCode: Optional[str] = Field(default=None, description="外部货品编码")


class OpenScmWareListSchema(BaseModel):
    size: Optional[int] = Field(default=None, description="每页大小， 最大100")
    page: Optional[int] = Field(default=None, description="第几页， 最大100")


class OpenScmWareUpdateSchema(BaseModel):
    wareVolume: Optional[Union[int, float]] = Field(default=None, description="货品体积，单位立方厘米，不超过10位数")
    wareName: Optional[str] = Field(default=None, description="货品名称")
    wareHeight: Optional[Union[int, float]] = Field(default=None, description="货品高度，单位厘米，不超过6位数")
    wareWidth: Optional[Union[int, float]] = Field(default=None, description="货品宽度，单位厘米，不超过6位数")
    wareOutCode: Optional[str] = Field(default=None, description="外部仓库编码")
    ownerSourceName: Optional[str] = Field(default=None, description="源头供货商名称")
    wareLength: Optional[Union[int, float]] = Field(default=None, description="货品长度，单位厘米，不超过6位数")
    ownerSourceTypeEnum: Optional[str] = Field(default=None, description="源头供货商类型，枚举值：1、工厂采购 MANUFACTORY_PURCHASE，2、品牌直供BRAND_DIRECT_SUPPLY，3、品牌经销BRAND_DEAL")
    barcode: Optional[str] = Field(default=None, description="条形码")
    wareWeight: Optional[Union[int, float]] = Field(default=None, description="货品重量，单位克，不超过6位数")


class OpenScmWarehouseAddSchema(BaseModel):
    contactName: Optional[str] = Field(default=None, description="联系人，命名规则需满足^[a-zA-Z一-龥]+$")
    address: Optional[str] = Field(default=None, description="地址")
    areaCode: Optional[str] = Field(default=None, description="区域编码，三级地址编码")
    townCode: Optional[str] = Field(default=None, description="街道编码，四级地址编码（使用前请联系平台开通四级地址服务）")
    name: Optional[str] = Field(default=None, description="仓库名称，命名规则需满足^[a-zA-Z0-9_\-一-龥]+$")
    postcode: Optional[str] = Field(default=None, description="邮编，命名规则需满足[1-9]\d{5}")
    alias: Optional[str] = Field(default=None, description="仓库别名，命名规则需满足^[a-zA-Z0-9_\-一-龥]+$")
    outCode: Optional[str] = Field(default=None, description="外部编码，命名规则需满足^[a-zA-Z0-9_\-]+$")
    contactTel: Optional[str] = Field(default=None, description="联系人电话，命名规则需满足 (\+\d+)?(\d{3,4}\-?)?\d{7,8}$")


class OpenScmWarehouseDeleteSchema(BaseModel):
    outCode: Optional[str] = Field(default=None, description="外部编码，命名规则需满足^[a-zA-Z0-9_\-]+$")


class OpenScmWarehouseInfoSchema(BaseModel):
    outCode: Optional[str] = Field(default=None, description="外部仓库编码，两个编码必传一个")
    code: Optional[str] = Field(default=None, description="快手仓库编码，两个编码必传一个")


class OpenScmWarehouseQuerySchema(BaseModel):
    size: Optional[int] = Field(default=None, description="每一页的数量，默认10,最大100")
    page: Optional[int] = Field(default=None, description="当前页，默认0，最大100")


class OpenScmWarehouseSalescopetemplateInfoSchema(BaseModel):
    outCode: Optional[str] = Field(default=None, description="外部仓库编码")


class AddressDTO(BaseModel):
    areaCode: Optional[str] = Field(default=None, description="区域编码")
    cityCode: Optional[str] = Field(default=None, description="城市编码")
    provinceCode: Optional[str] = Field(default=None, description="省份编码")
    townCode: Optional[str] = Field(default=None, description="街道编码，四级地址编码（使用前请联系平台开通四级地址服务）")


class OpenScmWarehouseSalescopetemplateOperationSchema(BaseModel):
    addressList: Optional[List[AddressDTO]] = Field(default=None, description="地址列表,每个地址，省市区只能有一个。设置省编码时， 会覆盖省下面的市和区。设置市编码同理。")
    outCode: Optional[str] = Field(default=None, description="外部仓库编码")


class OpenScmWarehouseUpdateSchema(BaseModel):
    contactName: Optional[str] = Field(default=None, description="联系人，命名规则需满足^[a-zA-Z一-龥]+$")
    address: Optional[str] = Field(default=None, description="地址")
    areaCode: Optional[str] = Field(default=None, description="区域编码，三级地址编码")
    name: Optional[str] = Field(default=None, description="仓库名称，命名规则需满足^[a-zA-Z0-9_\-一-龥]+$")
    postcode: Optional[str] = Field(default=None, description="邮编，命名规则需满足[1-9]\d{5}")
    alias: Optional[str] = Field(default=None, description="仓库别名，命名规则需满足^[a-zA-Z0-9_\-一-龥]+$")
    outCode: Optional[str] = Field(default=None, description="外部编码，命名规则需满足^[a-zA-Z0-9_\-]+$")
    contactTel: Optional[str] = Field(default=None, description="联系人电话，命名规则需满足 (\+\d+)?(\d{3,4}\-?)?\d{7,8}$")
    townCode: Optional[str] = Field(default=None, description="街道编码，四级地址编码（使用前请联系平台开通四级地址服务）")
