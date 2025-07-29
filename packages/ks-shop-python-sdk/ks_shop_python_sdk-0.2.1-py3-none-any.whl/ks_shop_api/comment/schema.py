# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional, List, Union


class ItemCommentOutInfo(BaseModel):
    outItemSkuId: Optional[int] = Field(default=None, description="业务方SKUID")
    outOrderNo: Optional[str] = Field(default=None, description="业务方订单编号")


class CreateOption(BaseModel):
    sourceType: Optional[int] = Field(default=None, description="类型")


class OpenCommentAddSchema(BaseModel):
    outInfo: Optional[ItemCommentOutInfo] = Field(default=None, description="业务参数")
    replyToCommentId: Optional[int] = Field(default=None, description="回复的评价ID")
    content: Optional[str] = Field(default=None, description="评价内容")
    option: Optional[CreateOption] = Field(default=None, description="扩展参数")


class OpenCommentListGetSchema(BaseModel):
    outOrderNo: Optional[str] = Field(default=None, description="订单id")
    serviceScore: Optional[list[int]] = Field(default=None, description="服务评分")
    qualityScore: Optional[list[int]] = Field(default=None, description="商品质量评分")
    logisticsScore: Optional[list[int]] = Field(default=None, description="物流评分")
    offset: Optional[int] = Field(default=None, description="偏移量. 页数*limit")
    limit: Optional[int] = Field(default=None, description="每页返回最大数目，最大20")
    createTimeFrom: Optional[int] = Field(default=None, description="评论创建时间from")
    createTimeTo: Optional[int] = Field(default=None, description="评论创建时间to")
    classifyType: Optional[int] = Field(default=None, description="分类类型 UNKNOWN_CLASSIFY_TYPE = 0; // 全部 REPLIED_CLASSIFY = 1; // 已回复 NO_REPLIED_CLASSIFY = 2; // 未回复 ATTACHED_CLASSIFY = 3; // 有追评 COMPLAIN_CLASSIFY = 4; // 已投诉")
    outItemId: Optional[int] = Field(default=None, description="商品id")
    itemTitle: Optional[str] = Field(default=None, description="商品名称")
    rootCommentTag: Optional[List[int]] = Field(default=None, description="主评论的标签")
    complainStatus: Optional[int] = Field(default=None, description="评论申诉状态 NO_COMPLAIN_YET = 0; // 暂无投诉 AUDITING_COMPLAIN = 1; // 投诉审核中 THROUGH_COMPLAIN = 2; // 投诉审核通过 REJECT_COMPLAIN = 3; // 投诉审核拒绝 MODIFY_COMPLAIN = 4; // 审核驳回待修改 UNKNOWN_COMPLAIN_STATUS = 5; // 全部")


class OpenSubcommentListGetSchema(BaseModel):
    rootCommentId: Optional[int] = Field(default=None, description="主评论ID")
    itemSkuId: Optional[int] = Field(default=None, description="商品SKU ID")
