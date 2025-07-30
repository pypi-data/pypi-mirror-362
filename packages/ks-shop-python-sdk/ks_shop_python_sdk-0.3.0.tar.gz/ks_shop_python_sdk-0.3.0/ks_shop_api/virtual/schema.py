# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional, List, Union


class IntegrationVirtualTopupMobileOrderCallbackSchema(BaseModel):
    orderId: Optional[str] = Field(default=None, description="订单ID")
    status: Optional[str] = Field(default=None, description="充值状态")
    bizType: Optional[str] = Field(default=None, description="10-快充，20-慢充")
    failCode: Optional[str] = Field(default=None, description="充值失败的错误码，详见对接文档")
    failMsg: Optional[str] = Field(default=None, description="充值失败的错误信息")


class AvailableEticket(BaseModel):
    code: Optional[str] = Field(default=None, description="电子凭证实体编号")
    num: Optional[int] = Field(default=None, description="核销数量")
    id: Optional[str] = Field(default=None, description="电子凭证虚拟卡编号")


class OpenVirtualEticketCheckavailableSchema(BaseModel):
    buyerId: Optional[int] = Field(default=None, description="买家编号")
    eticketType: Optional[str] = Field(default=None, description="电子凭证类型")
    etickets: Optional[List[AvailableEticket]] = Field(default=None, description="电子凭证列表")
    orderId: Optional[int] = Field(default=None, description="订单编号")
    sellerId: Optional[int] = Field(default=None, description="卖家编号")
