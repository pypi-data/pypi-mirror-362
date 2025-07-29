# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional, List, Union


class SupplierCategoryInfo(BaseModel):
    categoryName: Optional[str] = Field(default=None, description="类目名")
    categoryId: Optional[str] = Field(default=None, description="类目外部id")
    offlineState: Optional[int] = Field(default=None, description="类目外部状态 0在线 1离线")
    sortNumber: Optional[int] = Field(default=None, description="排序方式 默认从大到小排序")


class SyncOutSpuInfo(BaseModel):
    maxPrice: Optional[Union[int, float]] = Field(default=None, description="最高价")
    categoryName: Optional[str] = Field(default=None, description="当前spu所属类目名目名称")
    spuName: Optional[str] = Field(default=None, description="spu名称")
    offlineState: Optional[int] = Field(default=None, description="状态0为上线 1为下线")
    categoryId: Optional[str] = Field(default=None, description="当前spu所属类目id")
    sortNumber: Optional[int] = Field(default=None, description="从大到小排序")
    imgUrl: Optional[str] = Field(default=None, description="图片链接")
    outCateInfos: Optional[List[SupplierCategoryInfo]] = Field(default=None, description="外部类目信息")
    firstCateType: Optional[int] = Field(default=None, description="一级类目所属类型1: 3c 2大家电")
    type: Optional[int] = Field(default=None, description="1、修改了基本信息图片/名称/最高价等 2、上下架产生变化 3、问卷修改过")
    spuId: Optional[str] = Field(default=None, description="spu外部id")


class OpenIndustryTradeInSyncSpuInfoSchema(BaseModel):
    skuInfoList: Optional[List[SyncOutSpuInfo]] = Field(default=None, description="sku信息列表")


class DecryptParam(BaseModel):
    encryptedData: Optional[str] = Field(default=None, description="密文")
    sceneType: Optional[int] = Field(default=None, description="解密场景：1代表订单收件人信息（收件人姓名、地址、手机号），2代表实名信息（身份证号和姓名）")


class OpenIndustryVirtualOrderDecryptSchema(BaseModel):
    decryptList: Optional[List[DecryptParam]] = Field(default=None, description="解密参数")
    orderId: Optional[int] = Field(default=None, description="快手订单号")


class OpenIndustryVirtualOrderDetailSchema(BaseModel):
    orderId: Optional[int] = Field(default=None, description="快手订单号")


class OpenIndustryVirtualOrderReviewSchema(BaseModel):
    reviewCode: Optional[int] = Field(default=None, description="审核错误码")
    orderId: Optional[int] = Field(default=None, description="订单id")
