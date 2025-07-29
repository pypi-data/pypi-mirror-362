# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional, List, Union


class OpenCsLogisticsSessionCloseSchema(BaseModel):
    ksSessionId: Optional[str] = Field(default=None, description="快手会话ID")
    sessionId: Optional[str] = Field(default=None, description="物流公司会话ID")
    closeType: Optional[int] = Field(default=None, description="关闭类型")


class OpenCsLogisticsSessionCreateCallbackSchema(BaseModel):
    assistantId: Optional[str] = Field(default=None, description="客服工号")
    ksSessionId: Optional[str] = Field(default=None, description="快手会话ID")
    sessionId: Optional[str] = Field(default=None, description="物流公司会话ID")
    sessionType: Optional[int] = Field(default=None, description="会话分配结果类型")


class OpenCsLogisticsSessionMessagePullSchema(BaseModel):
    ksSessionId: Optional[str] = Field(default=None, description="快手会话ID")
    sessionId: Optional[str] = Field(default=None, description="物流公司会话ID")


class OpenCsLogisticsSessionMessageSendSchema(BaseModel):
    img: Optional[str] = Field(default=None, description="图片")
    contentType: Optional[int] = Field(default=None, description="消息类型")
    ksSessionId: Optional[str] = Field(default=None, description="快手会话ID")
    sessionId: Optional[str] = Field(default=None, description="物流公司会话ID")
    text: Optional[str] = Field(default=None, description="文本")
