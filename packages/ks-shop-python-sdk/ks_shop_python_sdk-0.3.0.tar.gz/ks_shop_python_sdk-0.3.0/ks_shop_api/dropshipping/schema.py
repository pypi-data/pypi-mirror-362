# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional, List, Union


class ItemDTO(BaseModel):
    itemLength: Optional[Union[int, float]] = Field(default=None, description="商品长度")
    itemWidth: Optional[Union[int, float]] = Field(default=None, description="商品宽度")
    itemWeight: Optional[Union[int, float]] = Field(default=None, description="商品重量")
    itemSpecs: Optional[str] = Field(default=None, description="商品规格")
    itemVolume: Optional[Union[int, float]] = Field(default=None, description="商品体积")
    itemTitle: Optional[str] = Field(default=None, description="商品名称")
    itemQuantity: Optional[int] = Field(default=None, description="商品数量")
    itemHeight: Optional[Union[int, float]] = Field(default=None, description="商品高度")


class AddressDTO(BaseModel):
    detailAddress: Optional[str] = Field(default=None, description="详细地址")
    addressId: Optional[str] = Field(default=None, description="地址ID")
    cityCode: Optional[str] = Field(default=None, description="城市编码")
    provinceCode: Optional[str] = Field(default=None, description="省份编码")
    streetCode: Optional[str] = Field(default=None, description="街道编码")
    streetName: Optional[str] = Field(default=None, description="街道名称")
    provinceName: Optional[str] = Field(default=None, description="省份名称")
    countryCode: Optional[str] = Field(default=None, description="国家编码")
    districtName: Optional[str] = Field(default=None, description="区县名称")
    cityName: Optional[str] = Field(default=None, description="城市名称")
    districtCode: Optional[str] = Field(default=None, description="区县编码")
    countryName: Optional[str] = Field(default=None, description="国家名称")


class Contract(BaseModel):
    name: Optional[str] = Field(default=None, description="	姓名")
    mobile: Optional[str] = Field(default=None, description="手机号码")
    telephone: Optional[str] = Field(default=None, description="电话")


class WarehouseDTO(BaseModel):
    warehouseOrderId: Optional[str] = Field(default=None, description="仓库订单号")
    warehouseCode: Optional[str] = Field(default=None, description="仓库编号")
    consignType: Optional[int] = Field(default=None, description="发货方式 (1、普通；2、仓库发货)")


class ExpressServiceDTO(BaseModel):
    code: Optional[str] = Field(default=None, description="编码")
    name: Optional[str] = Field(default=None, description="名称")
    value: Optional[str] = Field(default=None, description="增值服务值")


class DsOrderGetRequest(BaseModel):
    reserveEndTime: Optional[int] = Field(default=None, description="要求上门取件时间结束时间（邮政、京东）")
    totalPackageQuantity: Optional[int] = Field(default=None, description="包裹总数量（包括母单和子单数）")
    userName: Optional[str] = Field(default=None, description="代发商家名称")
    allocateOrderCode: Optional[str] = Field(default=None, description="代发订单编码")
    goodsDescription: Optional[str] = Field(default=None, description="大件快递货品描述")
    packagingDescription: Optional[str] = Field(default=None, description="大件快递的包装信息")
    totalPackageLength: Optional[Union[int, float]] = Field(default=None, description="包裹总长度")
    packageCode: Optional[str] = Field(default=None, description="包裹号（或者ERP订单号）")
    expressProductCode: Optional[str] = Field(default=None, description="物流产品编码")
    userCode: Optional[str] = Field(default=None, description="代发商家编码")
    itemList: Optional[List[ItemDTO]] = Field(default=None, description="商品列表")
    extData: Optional[str] = Field(default=None, description="扩展信息")
    hasFreightInsurance: Optional[bool] = Field(default=None, description="是否有运费险")
    netSiteName: Optional[str] = Field(default=None, description="网点名称")
    expressCompanyCode: Optional[str] = Field(default=None, description="物流公司编码")
    totalPackageWidth: Optional[Union[int, float]] = Field(default=None, description="包裹总宽度")
    orderChannel: Optional[str] = Field(default=None, description="订单渠道")
    podModelAddress: Optional[AddressDTO] = Field(default=None, description="回单服务地址")
    senderContract: Optional[Contract] = Field(default=None, description="发货人联系方式")
    totalPackageWeight: Optional[Union[int, float]] = Field(default=None, description="包裹总重量")
    tradeOrderRemark: Optional[str] = Field(default=None, description="订单备注信息")
    totalPackageVolume: Optional[Union[int, float]] = Field(default=None, description="包裹总体积")
    isSignBack: Optional[bool] = Field(default=None, description="是否签回单标识")
    payAmount: Optional[Union[int, float]] = Field(default=None, description="到付运费金额")
    settleAccount: Optional[str] = Field(default=None, description="客户编码 (所有直营)")
    payMethod: Optional[int] = Field(default=None, description="支付方式")
    warehouse: Optional[WarehouseDTO] = Field(default=None, description="仓或门店信息")
    totalPackageHeight: Optional[Union[int, float]] = Field(default=None, description="包裹总高度")
    netSiteCode: Optional[str] = Field(default=None, description="加盟物流公司网点编码")
    senderAddress: Optional[AddressDTO] = Field(default=None, description="发货地址信息")
    templateUrl: Optional[str] = Field(default=None, description="标准模板URL")
    reserveTime: Optional[int] = Field(default=None, description="要求上门取件时间")
    requestId: Optional[str] = Field(default=None, description="请求ID，唯一性标识")
    expressServices: Optional[List[ExpressServiceDTO]] = Field(default=None, description="增值服务")


class OpenDropshippingEbillBatchGetSchema(BaseModel):
    dsOrderGetReq: Optional[DsOrderGetRequest] = Field(default=None, description="请求列表")


class OpenDropshippingEbillCancelSchema(BaseModel):
    waybillCode: Optional[str] = Field(default=None, description="电子面单号")
    expressCompanyCode: Optional[str] = Field(default=None, description="物流公司编码")
    userCode: Optional[str] = Field(default=None, description="代发商家编码")


class OpenDropshippingOrderBatchAllocateSchema(BaseModel):
    dropshippingOrderCodeList: Optional[List[str]] = Field(default=None, description="代发订单编号列表，注意代发订单编号不是订单接口返回的oid，而是从代发订单列表/代发订单详情获取的，使用代发接口发货、取号、分配时需要使用dropshippingOrderCode（代发编号）")
    factoryCode: Optional[str] = Field(default=None, description="厂家编码")


class OpenDropshippingOrderBatchAllocateCancelSchema(BaseModel):
    dropshippingOrderCodeList: Optional[List[str]] = Field(default=None, description="代发订单编号列表，注意代发订单编号不是订单接口返回的oid，而是从代发订单列表/代发订单详情获取的，使用代发接口发货、取号、分配时需要使用dropshippingOrderCode（代发编号）")
    cancelAllocateReason: Optional[str] = Field(default=None, description="取消分配原因")


class DropshippingItemDTO(BaseModel):
    skuId: Optional[int] = Field(default=None, description="快手商品skuid")
    skuDesc: Optional[str] = Field(default=None, description="sku商品规格快照")
    skuNick: Optional[str] = Field(default=None, description="sku编码")
    skuNum: Optional[int] = Field(default=None, description="sku数量")
    itemId: Optional[int] = Field(default=None, description="商品id")
    itemTitle: Optional[str] = Field(default=None, description="商品名称")
    itemPicUrl: Optional[str] = Field(default=None, description="商品图片地址")


class AppendDropshippingOrderRequest(BaseModel):
    requestId: Optional[str] = Field(default=None, description="请求ID")
    dropshippingOrderCode: Optional[str] = Field(default=None, description="代发订单编号")
    orderType: Optional[int] = Field(default=None, description="追加的订单类型")
    orderItemList: Optional[List[DropshippingItemDTO]] = Field(default=None, description="订单商品信息")
    sellerNote: Optional[str] = Field(default=None, description="卖家备注")
    receiverAddress: Optional[AddressDTO] = Field(default=None, description="收货地址")
    receiverContact: Optional[Contract] = Field(default=None, description="收货人信息")


class OpenDropshippingOrderBatchAppendSchema(BaseModel):
    appendRequestList: Optional[List[AppendDropshippingOrderRequest]] = Field(default=None, description="追加列表")


class OpenDropshippingOrderBatchDeleteSchema(BaseModel):
    dropshippingOrderCodeList: Optional[List[str]] = Field(default=None, description="代发订单编号列表（<=10个）")


class OpenDropshippingOrderDeliverSchema(BaseModel):
    returnAddressId: Optional[int] = Field(default=None, description="退货地址id")
    waybillCode: Optional[str] = Field(default=None, description="电子面单号")
    userCode: Optional[str] = Field(default=None, description="代发商家编码")
    allocateOrderCode: Optional[str] = Field(default=None, description="代发订单编码")
    expressCompanyCode: Optional[str] = Field(default=None, description="物流公司编码")
    serialNumberList: Optional[List[str]] = Field(default=None, description="SN码列表，30位以内字符，当代发订单详情和列表API出参serialNumberInfo.serialType（商品码类型）值包含[1]时，发货必传SN码")
    imeiList: Optional[List[str]] = Field(default=None, description="IMEI码列表，15-17位数字，当代发订单详情和列表API出参serialNumberInfo.serialType（商品码类型）值包含[2]时，发货必传IMEI码")


class OpenDropshippingOrderDetailQuerySchema(BaseModel):
    allocateOrderCode: Optional[str] = Field(default=None, description="代发订单编码")
    userCode: Optional[str] = Field(default=None, description="代发商家编码")


class OpenDropshippingOrderListSchema(BaseModel):
    pageSize: Optional[int] = Field(default=None, description="每页数据数（不超过50）")
    beginTime: Optional[int] = Field(default=None, description="queryType的开始时间，单位毫秒，不能小于60天前，且需要小于结束时间，与结束时间间隔小于30分钟。")
    endTime: Optional[int] = Field(default=None, description="queryType的结束时间，单位毫秒，不能小于60天前。")
    queryType: Optional[int] = Field(default=None, description="查询类型[1:按分配时间查找][2:按更新时间查找]")
    sort: Optional[int] = Field(default=None, description="排序类型[1:时间降序][2:时间升序]（默认降序）")
    allocateStatus: Optional[int] = Field(default=None, description="订单分配状态[2:已取消][3:已分配未回传][4:已回传]（不传则代表查询所有状态订单）")
    cursor: Optional[str] = Field(default=None, description="游标内容，第一次传空串，之后传上一次的cursor返回值，若返回“nomore”则标识到底")


class OpenDropshippingOrderLogisticsUpdateSchema(BaseModel):
    waybillCode: Optional[str] = Field(default=None, description="电子面单号")
    expressCompanyCode: Optional[str] = Field(default=None, description="物流公司编码")
    userCode: Optional[str] = Field(default=None, description="代发商家编码")
    allocateOrderCode: Optional[str] = Field(default=None, description="代发订单编码")


class OpenDropshippingOrderMerchantDetailSchema(BaseModel):
    dropshippingOrderCode: Optional[str] = Field(default=None, description="代发订单编号")


class OpenDropshippingOrderMerchantListSchema(BaseModel):
    cursor: Optional[str] = Field(default=None, description="游标内容（第一次传空串，之后传上一次的cursor返回值）")
    pageSize: Optional[int] = Field(default=None, description="每页最大条数")
    factoryCode: Optional[str] = Field(default=None, description="厂家编码")
    dropshippingStatus: Optional[int] = Field(default=None, description="代发状态：（0-全部状态）、（1-待分配）、（2-已取消分配）、（3-已分配未回传）、（4-已分配已回传）")
    orderStatus: Optional[int] = Field(default=None, description="订单状态：（0-全部状态）、（100-待发货）、（200-已发货）、（500-已关闭）")
    refundStatus: Optional[int] = Field(default=None, description="售后状态：（0-全部状态）、（100-无售后）、（200-售后中）、（500-售后完成）")
    orderType: Optional[int] = Field(default=None, description="订单类型：（100- 交易主单、200-赠品、300-补货、400-换货、1000-其它）")
    queryType: Optional[int] = Field(default=None, description="查询类型：PAT_TIME-按支付时间 CREATE_TIME-按创建时间备注：需与beginTime与endTime配合使用")
    beginTime: Optional[int] = Field(default=None, description="查询起始时间，单位毫秒（查询起始时间大于0）")
    endTime: Optional[int] = Field(default=None, description="查询结束时间，单位毫秒（查询结束时间不小于查询起始时间且查询结束时间与查询起始时间间隔小于30天）")
    sort: Optional[int] = Field(default=None, description="排序方式 （0 时间降序 1 时间升序，默认0降序）")


class OpenDropshippingRelationListSchema(BaseModel):
    factoryCode: Optional[str] = Field(default=None, description="厂家编码")
    beginApplyTime: Optional[int] = Field(default=None, description="申请绑定起始时间")
    endApplyTime: Optional[int] = Field(default=None, description="申请绑定结束时间")
    pageIndex: Optional[int] = Field(default=None, description="第几页")
    pageSize: Optional[int] = Field(default=None, description="每页条数")


class ApplyBindFactoryRequest(BaseModel):
    requestId: Optional[str] = Field(default=None, description="请求ID")
    factoryCode: Optional[str] = Field(default=None, description="厂家编码")
    applyContent: Optional[str] = Field(default=None, description="申请绑定说明")


class OpenDropshippingRelationMerchantBatchApplySchema(BaseModel):
    applyRequestList: Optional[List[ApplyBindFactoryRequest]] = Field(default=None, description="绑定申请列表")


class UnbindFactoryRequest(BaseModel):
    requestId: Optional[str] = Field(default=None, description="请求ID")
    factoryCode: Optional[str] = Field(default=None, description="厂家编码")
    unboundReason: Optional[str] = Field(default=None, description="解除绑定说明")


class OpenDropshippingRelationMerchantBatchUnbindSchema(BaseModel):
    unbindRequestList: Optional[List[UnbindFactoryRequest]] = Field(default=None, description="解除绑定列表")


class OpenDropshippingRoleQuerySchema(BaseModel):
    pass
