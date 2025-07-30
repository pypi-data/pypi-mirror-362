# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional, List, Union


class OpenLiveShopItemCheckOncarSchema(BaseModel):
    itemId: Optional[int] = Field(default=None, description="需要判断的商品id")


class OpenLiveShopSellerRealUvSchema(BaseModel):
    pass


class OpenLieShopUserCarActionSchema(BaseModel):
    userOpenId: Optional[str] = Field(default=None, description="用户id")
    actionScene: Optional[List[int]] = Field(default=None, description="1:用户是否点击小黄车 2:用户是否加购小黄车景")


class OpenLiveShopWatchTimeMatchSchema(BaseModel):
    userOpenId: Optional[str] = Field(default=None, description="用户id")
    threshold: Optional[int] = Field(default=None, description="阈值(单位:秒)")
