# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional, List, Union


class OpenExpressCustomTempateListQuerySchema(BaseModel):
    standardTemplateCode: Optional[str] = Field(default=None, description="标准模板code")
    type: Optional[int] = Field(default=None, description="查询类型，（1：商家自定义模板；2：ISV预设自定义模板；3：商家+ISV全部自定义模板）")


class OpenExpressEbillAppendSchema(BaseModel):
    parentWaybillCode: Optional[str] = Field(default=None, description="母电子面单号")
    expressCompanyCode: Optional[str] = Field(default=None, description="物流公司编码")
    addPackageQuantity: Optional[int] = Field(default=None, description="新增加子面单个数（大于0）")


class OpenExpressEbillCancelSchema(BaseModel):
    expressCompanyCode: Optional[str] = Field(default=None, description="物流公司编码")
    waybillCode: Optional[str] = Field(default=None, description="运单号")


class ItemDTO(BaseModel):
    itemLength: Optional[Union[int, float]] = Field(default=None, description="商品长度")
    itemWidth: Optional[Union[int, float]] = Field(default=None, description="商品宽度")
    itemHeight: Optional[Union[int, float]] = Field(default=None, description="商品高度")
    itemWeight: Optional[Union[int, float]] = Field(default=None, description="商品重量")
    itemSpecs: Optional[str] = Field(default=None, description="商品规格")
    itemVolume: Optional[Union[int, float]] = Field(default=None, description="商品体积")
    itemTitle: Optional[str] = Field(default=None, description="商品名称")
    itemQuantity: Optional[int] = Field(default=None, description="商品数量")


class Contract(BaseModel):
    name: Optional[str] = Field(default=None, description="	姓名，支持密文，对应订单API出参encryptedConsignee")
    mobile: Optional[str] = Field(default=None, description="手机号码，支持密文，对应订单API出参encryptedMobile")
    telephone: Optional[str] = Field(default=None, description="电话，可以为空，只能传明文，不能传mobile的加密密文")


class AddressDTO(BaseModel):
    countryCode: Optional[str] = Field(default=None, description="国家编码")
    countryName: Optional[str] = Field(default=None, description="国家名称")
    provinceCode: Optional[str] = Field(default=None, description="省份编码")
    provinceName: Optional[str] = Field(default=None, description="省份名称")
    cityCode: Optional[str] = Field(default=None, description="城市编码")
    cityName: Optional[str] = Field(default=None, description="城市名称")
    districtCode: Optional[str] = Field(default=None, description="区县编码")
    districtName: Optional[str] = Field(default=None, description="区县名称")
    streetCode: Optional[str] = Field(default=None, description="街道编码")
    streetName: Optional[str] = Field(default=None, description="街道名称")
    detailAddress: Optional[str] = Field(default=None, description="详细地址，支持密文传输，对应订单API出参encryptedAddress")


class ExpressServiceDTO(BaseModel):
    code: Optional[str] = Field(default=None, description="增值服务编码")
    name: Optional[str] = Field(default=None, description="增值服务名称")
    value: Optional[str] = Field(default=None, description="增值服务对应的value")


class WarehouseDTO(BaseModel):
    consignType: Optional[int] = Field(default=None, description="发货方式 (1、普通；2、仓库发货；3、总对总-门店发货)")
    warehouseOrderId: Optional[str] = Field(default=None, description="仓库订单号")
    warehouseCode: Optional[str] = Field(default=None, description="仓库/门店编号")
    warehouseName: Optional[str] = Field(default=None, description="仓库/门店名称")
    consignNetSiteCode: Optional[str] = Field(default=None, description="发货网点编码")
    secretKey: Optional[str] = Field(default=None, description="月结账户密钥")


class GetEbillOrderRequest(BaseModel):
    merchantCode: Optional[str] = Field(default=None, description="商家编码（快手订单取订单信息中的sellerOpenId；线下订单为当前取号快手小店的商家ID）")
    merchantName: Optional[str] = Field(default=None, description="商家名称（快手订单取订单信息中的sellerNick；线下订单为当前取号快手小店的商家名称）")
    totalPackageQuantity: Optional[int] = Field(default=None, description="包裹总数量（包括母单和子单数，直营物流公司必传；加盟快运物流公司必传；加盟快递物流公司未强检验非空可不传，但建议规范化都传 1 ）")
    goodsDescription: Optional[str] = Field(default=None, description="大件快递货品描述")
    packagingDescription: Optional[str] = Field(default=None, description="大件快递的包装信息")
    totalPackageLength: Optional[Union[int, float]] = Field(default=None, description="包裹总长度（单位cm）")
    packageCode: Optional[str] = Field(default=None, description="包裹号，用来实现拆包功能：1.同一个交易订单下传递相同的包裹号会返回相同的运单号。2.如果需要同一个交易订单号下取不同的运单号需要传递不同的包裹号，可请求多次，每次传不同的包裹号")
    expressProductCode: Optional[str] = Field(default=None, description="物流产品类型(https://docs.qingque.cn/d/home/eZQA8Nj0UUPfQKMz6exheqrgZ?identityId=1hu1ksD6aDT#section=h.gwdkcr71e684)")
    itemList: Optional[List[ItemDTO]] = Field(default=None, description="商品信息列表")
    extData: Optional[str] = Field(default=None, description="面单扩展信息json格式（顺丰必传入 isvClientCode，是指顺丰分配的独立顾客编码，商家在和顺丰签订月结合同时需要额外向顺丰索取）（邮政必传入 oneBillFeeType:1）")
    receiverContract: Optional[Contract] = Field(default=None, description="收货人联系方式")
    senderContract: Optional[Contract] = Field(default=None, description="发货人联系方式")
    hasFreightInsurance: Optional[bool] = Field(default=None, description="	false：没有运费险true：有运费险（仅用于逆向场景）")
    netSiteCode: Optional[str] = Field(default=None, description="网点编码（加盟必须）")
    netSiteName: Optional[str] = Field(default=None, description="网点名称（加盟必须）")
    expressCompanyCode: Optional[str] = Field(default=None, description="快递公司编码，查看文档https://open.kwaixiaodian.com/solution/detail?pageSign=be565dfc5ca82ebb4683bc208f7929051642596657058#section-6")
    orderChannel: Optional[str] = Field(default=None, description="订单渠道(https://docs.qingque.cn/s/home/eZQCPgx29ls1rz4l7efnPfMiH?identityId=EmukFTnlEF)")
    podModelAddress: Optional[AddressDTO] = Field(default=None, description="签回单标识值：false-否；true-是 ；")
    totalPackageWidth: Optional[Union[int, float]] = Field(default=None, description="包裹总宽度(cm)")
    totalPackageWeight: Optional[Union[int, float]] = Field(default=None, description="包裹总重量(g)")
    tradeOrderRemark: Optional[str] = Field(default=None, description="订单备注信息(最多128字符)")
    totalPackageVolume: Optional[Union[int, float]] = Field(default=None, description="包裹总体积（单位cm³）")
    isSignBack: Optional[bool] = Field(default=None, description="签回单标识值：false-否；true-是 ；")
    payAmount: Optional[Union[int, float]] = Field(default=None, description="到付运费金额，单位为分")
    payMethod: Optional[int] = Field(default=None, description="支付方式（不同物流公司要求不同)，可以参考快手电子面单对接(https://docs.qingque.cn/d/home/eZQA8Nj0UUPfQKMz6exheqrgZ?identityId=21ZaUL9ME32#section=h.nhgxlpvk3yp9)的8.5、8.6")
    totalPackageHeight: Optional[Union[int, float]] = Field(default=None, description="包裹总高度(cm)")
    tradeOrderCode: Optional[str] = Field(default=None, description="订单编号，最大支持32个字符长度。若为快手订单，receiverAddress的收件人姓名、手机号和详细地址传输密文，仅支持快手主品订单id；若非快手订单，receiverAddress的收件人姓名、手机号和详细地址传输明文")
    senderAddress: Optional[AddressDTO] = Field(default=None, description="发货地址信息")
    templateUrl: Optional[str] = Field(default=None, description="标准模板模板URL")
    reserveTime: Optional[int] = Field(default=None, description="预约上门取件开始时间")
    reserveEndTime: Optional[int] = Field(default=None, description="预约上门取件时间结束时间")
    receiverAddress: Optional[AddressDTO] = Field(default=None, description="收货人地址信息")
    requestId: Optional[str] = Field(default=None, description="	请求唯一ID，字符串，长度不能超过128，要保证唯一，服务端做幂等使用。批量取号时候，列表里面的requestID要保证不重复")
    expressServices: Optional[List[ExpressServiceDTO]] = Field(default=None, description="	附加服务列表（https://docs.qingque.cn/d/home/eZQA8Nj0UUPfQKMz6exheqrgZ?identityId=1hu1ksD6aDT#section=h.gwdkcr71e684）")
    settleAccount: Optional[str] = Field(default=None, description="客户编码")
    warehouse: Optional[WarehouseDTO] = Field(default=None, description="仓或门店信息")


class OpenExpressEbillGetSchema(BaseModel):
    getEbillOrderRequest: Optional[List[GetEbillOrderRequest]] = Field(default=None, description="电子面单取号请求列表")


class OpenExpressEbillUpdateSchema(BaseModel):
    goodsDescription: Optional[str] = Field(default=None, description="大件快递货品描述")
    packagingDescription: Optional[str] = Field(default=None, description="大件快递的包装信息")
    totalPackageLength: Optional[Union[int, float]] = Field(default=None, description="包裹总长度（单位cm）")
    itemList: Optional[List[ItemDTO]] = Field(default=None, description="商品信息列表")
    extData: Optional[str] = Field(default=None, description="面单扩展信息")
    receiverContract: Optional[Contract] = Field(default=None, description="收货人联系方式")
    senderContract: Optional[Contract] = Field(default=None, description="发货人联系方式")
    expressCompanyCode: Optional[str] = Field(default=None, description="快递公司编码（不允许修改，见：https://open.kwaixiaodian.com/solution/detail?pageSign=be565dfc5ca82ebb4683bc208f7929051642596657058#section-6）")
    totalPackageWidth: Optional[Union[int, float]] = Field(default=None, description="包裹总宽度(cm)")
    totalPackageWeight: Optional[Union[int, float]] = Field(default=None, description="包裹总重量(g)")
    tradeOrderRemark: Optional[str] = Field(default=None, description="订单备注信息(最多128字符)")
    totalPackageVolume: Optional[Union[int, float]] = Field(default=None, description="包裹总体积（单位cm³）")
    totalPackageHeight: Optional[Union[int, float]] = Field(default=None, description="包裹总高度(cm)")
    receiverAddress: Optional[AddressDTO] = Field(default=None, description="收货人地址信息")
    waybillCode: Optional[str] = Field(default=None, description="物流运单号（不允许修改）")


class OpenExpressPrinterElementQuerySchema(BaseModel):
    pass


class QueryRoutingReachableRequest(BaseModel):
    requestId: Optional[str] = Field(default=None, description="请求ID（单次请求中必须唯一）")
    expressCompanyCode: Optional[str] = Field(default=None, description="物流公司编码（所有子请求中相同）")
    type: Optional[int] = Field(default=None, description="地址类型（0、揽收地址+派送地址；1、揽收地址；2、派送地址）")
    senderAddress: Optional[AddressDTO] = Field(default=None, description="发货地址信息")
    receiverAddress: Optional[AddressDTO] = Field(default=None, description="收货地址信息")
    expressProductCode: Optional[str] = Field(default=None, description="物流产品编码")
    expressServices: Optional[List[ExpressServiceDTO]] = Field(default=None, description="物流增值服务列表")


class OpenExpressReachableQuerySchema(BaseModel):
    reachableRequests: Optional[List[QueryRoutingReachableRequest]] = Field(default=None, description="请求列表（单次请求个数小于10）")


class OpenExpressStandardTemplateListGetSchema(BaseModel):
    expressCompanyCode: Optional[str] = Field(default=None, description="公司编码")


class OpenExpressSubscribeQuerySchema(BaseModel):
    expressCompanyCode: Optional[str] = Field(default=None, description="公司编码")
