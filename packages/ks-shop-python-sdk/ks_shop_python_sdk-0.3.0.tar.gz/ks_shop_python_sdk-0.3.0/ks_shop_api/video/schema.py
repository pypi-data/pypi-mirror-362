# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional, List, Union


class OpenPhotoCountSchema(BaseModel):
    pass


class OpenPhotoDeleteSchema(BaseModel):
    photoId: Optional[str] = Field(default=None, description="视频Id")


class OpenPhotoInfoSchema(BaseModel):
    photoId: Optional[str] = Field(default=None, description="作品id")


class OpenPhotoListSchema(BaseModel):
    cursor: Optional[str] = Field(default=None, description="游标，用于分页，值为作品id。分页查询时，传上一页create_time最小的photo_id。第一页不传此参数")
    count: Optional[int] = Field(default=None, description="数量，默认为20,最大不超过200")


class OpenPhotoPublishSchema(BaseModel):
    uploadToken: Optional[str] = Field(default=None, description="用户唯一标识")


class OpenPhotoStartUploadSchema(BaseModel):
    pass
