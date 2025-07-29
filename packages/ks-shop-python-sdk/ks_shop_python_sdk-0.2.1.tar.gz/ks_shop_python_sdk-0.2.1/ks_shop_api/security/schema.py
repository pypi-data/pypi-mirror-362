# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional, List, Union


class PeriodDecryptData(BaseModel):
    encryptedData: Optional[str] = Field(default=None, description="密文信息")


class OpenSecurityInstantDecryptBatchSchema(BaseModel):
    decryptDataList: Optional[List[PeriodDecryptData]] = Field(default=None, description="批量解密list，每次请求，报文条数不超过100条。")


class OpenSecurityLogBatchSchema(BaseModel):
    method: Optional[str] = Field(default=None, description="批量上传的日志方法名字标示，order、open、sql、login")
    data: Optional[str] = Field(default=None, description="日志内容，字段结构对齐method对应接口的入参字段结构，每次最多100条记录，如果超过100条，请拆分成多条请求。")


class OpenSecurityLogLoginSchema(BaseModel):
    openId: Optional[str] = Field(default=None, description="商家在快手的唯一标识，在同一开发主体下唯一。优先使用openId字段，如没有改字段则使用sellerId字段，openId和sellerId不许均为空")
    sellerId: Optional[int] = Field(default=None, description="	商家id（主子账号共用同一个商家id，替换原有url中的shopId即sellerId）")
    userIp: Optional[str] = Field(default=None, description="登陆用户IP地址，请注意要记录用户客户端的IP，不是记录ISV自身服务器的IP。")
    loginResult: Optional[str] = Field(default=None, description="登陆状态成功、失败")
    loginMessage: Optional[str] = Field(default=None, description="额外信息，如失败原因")
    time: Optional[int] = Field(default=None, description="登陆操作时间，整型时间戳，精确到毫秒")


class OpenSecurityLogOpenSchema(BaseModel):
    openId: Optional[str] = Field(default=None, description="商家在快手的唯一标识，在同一开发主体下唯一。优先使用openId字段，如没有改字段则使用sellerId字段，openId和sellerId不许均为空")
    sellerId: Optional[int] = Field(default=None, description="商家id（主子账号共用同一个商家id，替换原有url中的shopId即sellerId）")
    userId: Optional[str] = Field(default=None, description="ISV自建开放平台场景，没有sellerId及其openId时需填充的字段且该字段需能定位到具体用户")
    orderIds: Optional[List[int]] = Field(default=None, description="用户操作订单Id，用英文逗号分隔，每次最多100条记录。如果超过100条，请拆分成多条请求。要求传入的订单Id为快手的原始单号。orderIds和data字段不许均为空。")
    clientIp: Optional[str] = Field(default=None, description="数据接收方IP地址，请注意要记录用户客户端的IP，不是记录ISV自身服务器的IP。")
    data: Optional[str] = Field(default=None, description="批量同步等涉及大批订单场景，orderIds字段可为空，将订单筛选条件填充到data字段中、订单总量填充到orderTotal字段中。orderIds和data字段不许均为空。")
    orderTotal: Optional[int] = Field(default=None, description="订单总量")
    url: Optional[str] = Field(default=None, description="客户端请求url")
    sendToUrl: Optional[str] = Field(default=None, description="订单推送目的地URL")
    time: Optional[int] = Field(default=None, description="操作时间，整型时间戳，精确到毫秒")


class OpenSecurityLogOrderSchema(BaseModel):
    openId: Optional[str] = Field(default=None, description="商家在快手的唯一标识，在同一开发主体下唯一。优先使用openId字段，如没有改字段则使用sellerId字段，openId和sellerId不许均为空")
    sellerId: Optional[int] = Field(default=None, description="商家id（主子账号共用同一个商家id，替换原有url中的shopId即sellerId）")
    url: Optional[str] = Field(default=None, description="用户操作URL。对于CS架构等没有url场景可以硬编码一个和贵司相关联的域名做替代。")
    userIp: Optional[str] = Field(default=None, description="用户IP地址，请注意要记录用户客户端的IP，不是记录ISV自身服务器的IP。")
    orderIds: Optional[List[int]] = Field(default=None, description="用户操作订单Id，用英文逗号分隔，每次最多100条记录。如果超过100条，请拆分成多条请求。要求传入的订单Id为快手的原始单号。orderIds和data字段不许均为空。")
    operation: Optional[int] = Field(default=None, description="用户操作说明，该字段请参考当前页面的请求示例-JSON卡片内容或《开放平台日志接入规范》 - 订单操作类型说明表")
    data: Optional[str] = Field(default=None, description="订单导出、下载等涉及大批订单场景，orderIds字段可为空，将订单筛选条件填充到data字段中、订单总量填充到orderTotal字段中。orderIds和data字段不许均为空。")
    orderTotal: Optional[int] = Field(default=None, description="用户操作订单总量")
    time: Optional[int] = Field(default=None, description="用户操作时间，整型时间戳，精确到毫秒")


class OpenSecurityLogSqlSchema(BaseModel):
    type: Optional[str] = Field(default=None, description="数据库类型")
    sql: Optional[str] = Field(default=None, description="sql语句，仅需要记录由于用户前端操作所引发的数据库操作，尤其是针对订单操作，不需要记录后端逻辑自行产生的数据库操作。")
    time: Optional[int] = Field(default=None, description="操作时间，整型时间戳，精确到毫秒")
