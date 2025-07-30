# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional, List, Union


class OpenServiceMarketBuyerServiceInfoSchema(BaseModel):
    buyerOpenId: Optional[str] = Field(default=None, description="买家openId")


class OpenServiceMarketOrderDetailSchema(BaseModel):
    oid: Optional[int] = Field(default=None, description="订单id")


class OpenServiceMarketOrderListSchema(BaseModel):
    startTime: Optional[int] = Field(default=None, description="开始时间")
    endTime: Optional[int] = Field(default=None, description="结束时间")
    queryType: Optional[int] = Field(default=None, description="查询类型，1按创建时间查询，2按支付时间查询")
    status: Optional[int] = Field(default=None, description="订单状态，10待付款，30已付款，80已关闭")
    pageSize: Optional[int] = Field(default=None, description="每页数量，不大于100")
    pageNum: Optional[int] = Field(default=None, description="页码")
    buyerOpenId: Optional[str] = Field(default=None, description="买家openId")
