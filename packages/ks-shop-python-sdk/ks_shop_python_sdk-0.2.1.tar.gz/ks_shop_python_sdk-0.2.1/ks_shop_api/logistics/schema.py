# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional, List, Union


class OpenAddressDistrictListSchema(BaseModel):
    districtVersion: Optional[str] = Field(default=None, description="行政区划：2017, 2021。四级地址请传入2021版本")


class BaseAddressInfo(BaseModel):
    consignee: Optional[str] = Field(default=None, description="收货人姓名")
    mobile: Optional[str] = Field(default=None, description="收货人手机号")
    provinceCode: Optional[int] = Field(default=None, description="省份编码")
    province: Optional[str] = Field(default=None, description="省份名称")
    cityCode: Optional[int] = Field(default=None, description="市编码")
    city: Optional[str] = Field(default=None, description="市名称")
    districtCode: Optional[int] = Field(default=None, description="区编码")
    district: Optional[str] = Field(default=None, description="区名称")
    address: Optional[str] = Field(default=None, description="地址信息")
    town: Optional[str] = Field(default=None, description="街道名称")
    townCode: Optional[int] = Field(default=None, description="街道编码")
    addressMetaVersion: Optional[int] = Field(default=None, description="地址版本， 四级地址版本为202100，新增和编辑的地址为四级地址时必须传值")


class OpenAddressSellerCreateSchema(BaseModel):
    baseInfo: BaseAddressInfo = Field(default=None, description="商家地址信息")
    defaultAddress: Optional[bool] = Field(default=None, description="是否默认")
    addressType: Optional[int] = Field(default=None, description="地址类型：2-退货地址；3-发货地址")


class OpenAddressSellerDeleteSchema(BaseModel):
    addressId: Optional[int] = Field(default=None, description="地址ID")


class OpenAddressSellerGetSchema(BaseModel):
    addressId: Optional[int] = Field(default=None, description="地址ID")


class OpenAddressSellerListSchema(BaseModel):
    addressType: Optional[int] = Field(default=None, description="地址类型：2-退货地址；3-发货地址")


class OpenAddressSellerUpdateSchema(BaseModel):
    baseInfo: BaseAddressInfo = Field(default=None, description="商家地址信息")
    defaultAddress: Optional[bool] = Field(default=None, description="是否默认")
    addressType: Optional[int] = Field(default=None, description="地址类型：2-退货地址；3-发货地址")


class OpenLogisticsExpressTemplateAddSchema(BaseModel):
    sendProvinceName: Optional[str] = Field(default=None, description="省份名称")
    sendDistrictCode: Optional[int] = Field(default=None, description="区域编码（6位）")
    sendTime: Optional[int] = Field(default=None, description="	【已废弃】承诺发货时间，传0即可")
    sendCityName: Optional[str] = Field(default=None, description="市名称")
    calType: Optional[int] = Field(default=None, description="计费类型：1-按件计费；2-按重量计费")
    name: Optional[str] = Field(default=None, description="运费模板名称")
    sourceType: Optional[int] = Field(default=None, description="来源：10-Android； 20-iOS； 30-PCWEB； 40-SYSTEM")
    sendProvinceCode: Optional[int] = Field(default=None, description="	省份编码（2位）")
    sendCityCode: Optional[int] = Field(default=None, description="市编码（4位）")
    config: Optional[str] = Field(default=None, description="type：目前只有1一种；includeProvinces：包邮省（只能为省code）；excludeProvinces：不配送地区，历史数据有code（只能为省code），已迁移到codeList（支持省市区多级code），若有codeList字段，将以codeList计算运费； reasonCode：不配送原因（1-台风，2-距离，3-重量，4-国家会议，5-合作快递不配送该区域，6-合作快递该区域服务差，7-其他）； provinceFees：运费规则，历史数据有code（只能为省code），已迁移到codeList（支持省市区多级code），若有codeList字段，将以codeList计算运费； baseCount：起步件数； baseFee：起步运费（分） ；perAddCount：递增件数； perAddFee：递增运费金额（分）； includeCount：满N件包邮 ；includeFee：满N包邮（分）； includeUnit：count代表件，price代表钱")
    sendDistrictName: Optional[str] = Field(default=None, description="区名称")


class OpenLogisticsExpressTemplateDetailSchema(BaseModel):
    id: Optional[int] = Field(default=None, description="运费模板id")


class OpenLogisticsExpressTemplateListSchema(BaseModel):
    offset: Optional[int] = Field(default=None, description="偏移量。按照模板的创建时间倒序排列，最新创建的模板offset=0，次新的offset=1，以此类推")
    limit: Optional[int] = Field(default=None, description="返回的结果中的运费模板的个数")
    searchUsed: Optional[bool] = Field(default=None, description="false表示不查询运费模板的是否使用状态。所以当该值为false时，接口返回结果中的所有模板的used字段恒定为false")


class OpenLogisticsExpressTemplateSaleLimitSchema(BaseModel):
    pass


class OpenLogisticsExpressTemplateSaleLimitRemoveSchema(BaseModel):
    feeShipConfig: Optional[str] = Field(default=None, description="// ${baseCount}件内 ${baseFee} 元，每增加${perAddCount}件，加${perAddFee}元指定条件包邮：满 ${includeCount} ${includeUnit} 包邮")


class OpenLogisticsExpressTemplateUpdateSchema(BaseModel):
    sendDistrictCode: Optional[int] = Field(default=None, description="区域编码（6位）")
    sendCityName: Optional[str] = Field(default=None, description="市名称")
    calType: Optional[int] = Field(default=None, description="计费类型：1-按件计费；2-按重量计费")
    sourceType: Optional[int] = Field(default=None, description="来源：10-Android； 20-iOS； 30-PCWEB； 40-SYSTEM")
    sendProvinceCode: Optional[int] = Field(default=None, description="	省份编码（2位）")
    sendCityCode: Optional[int] = Field(default=None, description="市编码（4位）")
    sendDistrictName: Optional[str] = Field(default=None, description="区名称")
    sendProvinceName: Optional[str] = Field(default=None, description="省份名称")
    sendTime: Optional[int] = Field(default=None, description="	【已废弃】承诺发货时间，传0即可")
    name: Optional[str] = Field(default=None, description="运费模板名称")
    id: Optional[int] = Field(default=None, description="运费模板id")
    config: Optional[str] = Field(default=None, description="type：目前只有1一种；includeProvinces：包邮省（只能为省code）；excludeProvinces：不配送地区，历史数据有code（只能为省code），已迁移到codeList（支持省市区多级code），若有codeList字段，将以codeList计算运费； reasonCode：不配送原因（1-台风，2-距离，3-重量，4-国家会议，5-合作快递不配送该区域，6-合作快递该区域服务差，7-其他）； provinceFees：运费规则，历史数据有code（只能为省code），已迁移到codeList（支持省市区多级code），若有codeList字段，将以codeList计算运费； baseCount：起步件数； baseFee：起步运费（分） ；perAddCount：递增件数； perAddFee：递增运费金额（分）； includeCount：满N件包邮 ；includeFee：满N包邮（分）； includeUnit：count代表件，price代表钱")


class OpenLogisticsTroubleNetSitePageQuerySchema(BaseModel):
    cityCode: Optional[List[int]] = Field(default=None, description="市编码（4位）")
    expressCompanyCode: Optional[str] = Field(default=None, description="物流商编码")
    provinceCode: Optional[List[int]] = Field(default=None, description="省份编码（2位）")
    controlStatus: Optional[int] = Field(default=None, description="管控状态，1:不管控，2:预警中，3:暂停签约，4:冻结中")
    pageNo: Optional[int] = Field(default=None, description="页码")
    pageSize: Optional[int] = Field(default=None, description="页大小")
