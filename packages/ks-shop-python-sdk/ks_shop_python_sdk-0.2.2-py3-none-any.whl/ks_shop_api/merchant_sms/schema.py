# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional, List, Union


class OpenPublicTemplateViewSchema(BaseModel):
    templateId: Optional[str] = Field(default=None, description="模板ID")
    pageNum: Optional[int] = Field(default=None, description="页码")
    pageSize: Optional[int] = Field(default=None, description="每页数量")


class SmsItemRequest(BaseModel):
    extra: Optional[str] = Field(default=None, description="业务扩展字段，最大60")
    mobile: Optional[str] = Field(default=None, description="手机号，既可以是明文也可以是密文(平台接口返回的手机号密文)")


class OpenSmsBatchSendSchema(BaseModel):
    signId: Optional[int] = Field(default=None, description="签名ID")
    templateParam: Optional[str] = Field(default=None, description="模板参数 json")
    templateId: Optional[int] = Field(default=None, description="模板ID")
    itemRequest: Optional[List[SmsItemRequest]] = Field(default=None, description="发送手机号，最大20个")


class OpenSmsCrowdSendSchema(BaseModel):
    signId: Optional[int] = Field(default=None, description="签名ID")
    templateId: Optional[int] = Field(default=None, description="模板ID")
    templateParam: Optional[str] = Field(default=None, description="模板参数 json")
    crowdId: Optional[int] = Field(default=None, description="人群包ID")
    extra: Optional[str] = Field(default=None, description="业务扩展字段，最大60")


class OpenSmsExpressSendSchema(BaseModel):
    signId: Optional[int] = Field(default=None, description="签名ID")
    templateId: Optional[int] = Field(default=None, description="模板ID")
    templateParam: Optional[str] = Field(default=None, description="模板参数 json")
    waybillCode: Optional[str] = Field(default=None, description="运单号")
    extra: Optional[str] = Field(default=None, description="业务扩展字段，最大60")


class OpenSmsSendSchema(BaseModel):
    signId: Optional[int] = Field(default=None, description="签名ID")
    templateId: Optional[int] = Field(default=None, description="模板ID")
    templateParam: Optional[str] = Field(default=None, description="模板参数 json")
    mobile: Optional[str] = Field(default=None, description="手机号，既可以是明文也可以是密文(平台接口返回的手机号密文)")
    extra: Optional[str] = Field(default=None, description="业务扩展字段，最大60")


class OpenSmsSendResultSchema(BaseModel):
    messageId: Optional[int] = Field(default=None, description="消息id")
    templateId: Optional[int] = Field(default=None, description="模板ID")
    signId: Optional[int] = Field(default=None, description="签名ID")
    mobile: Optional[str] = Field(default=None, description="手机号，既可以是明文也可以是密文(平台接口返回的手机号密文)")
    status: Optional[int] = Field(default=None, description="短信状态：1未回执 2发送成功 3发送失败")
    startTime: Optional[int] = Field(default=None, description="开始时间(只能查最近1个月的记录)")
    endTime: Optional[int] = Field(default=None, description="结束时间（开始时间与结束时间间隔不能大于7天）")
    pageNum: Optional[int] = Field(default=None, description="页码")
    pageSize: Optional[int] = Field(default=None, description="每页多少条，最大50")


class OpenSmsSignApplyCreateSchema(BaseModel):
    sign: Optional[str] = Field(default=None, description="申请的短信签名，要和商家的店铺名称一致，不允许申请账号昵称或和商家商品无关的任何签名")


class OpenSmsSignDeleteSchema(BaseModel):
    signId: Optional[int] = Field(default=None, description="签名ID")


class OpenSmsSignViewSchema(BaseModel):
    signLike: Optional[str] = Field(default=None, description="签名的模糊搜索")
    pageNum: Optional[int] = Field(default=None, description="页码")
    pageSize: Optional[int] = Field(default=None, description="每页数量")
    signId: Optional[int] = Field(default=None, description="签名ID")


class OpenSmsTemplateApplyCreateSchema(BaseModel):
    templateName: Optional[str] = Field(default=None, description="模板名称")
    templateContent: Optional[str] = Field(default=None, description="模板内容，当模板类型为1-推广类，模板内容必须以“拒收请回复R”结尾")
    templateType: Optional[int] = Field(default=None, description="模板类型 1 推广类 2 通知类")


class OpenSmsTemplateDeleteSchema(BaseModel):
    templateId: Optional[int] = Field(default=None, description="模板ID")


class OpenSmsTemplateViewSchema(BaseModel):
    templateId: Optional[int] = Field(default=None, description="模板ID")
    templateName: Optional[str] = Field(default=None, description="模板名称")
    pageNum: Optional[int] = Field(default=None, description="页码")
    pageSize: Optional[int] = Field(default=None, description="每页数量")
