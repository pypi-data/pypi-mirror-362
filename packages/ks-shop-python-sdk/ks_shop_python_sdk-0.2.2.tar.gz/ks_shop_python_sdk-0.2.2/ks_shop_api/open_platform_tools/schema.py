# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional, List, Union


class WhiteIP(BaseModel):
    ip: Optional[str] = Field(default=None, description="ip，也支持ip段")
    status: Optional[int] = Field(None, description="状态，1:启用，2:停用")


class OpenToolWhiteipListAddSchema(BaseModel):
    whiteListIPS: Optional[List[WhiteIP]] = Field(default=None, description="白名单集合")
