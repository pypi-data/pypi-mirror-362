# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional, List, Union


class OpenInvoiceAmountGetSchema(BaseModel):
    fromType: Optional[str] = Field(default=None, description="1 商家 2 平台 3 达人 4 团长")
    toType: Optional[str] = Field(default=None, description="1 商家 2 用户 3 平台 4 达人 5 团长")
    toId: Optional[int] = Field(default=None, description="开票对象")
    orderId: Optional[int] = Field(default=None, description="订单ID")


class OpenInvoiceSubsidyAuditInfoSchema(BaseModel):
    oid: Optional[str] = Field(default=None, description="快手订单号")
