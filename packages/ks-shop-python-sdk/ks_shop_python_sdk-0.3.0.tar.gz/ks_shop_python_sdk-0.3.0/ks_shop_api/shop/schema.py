# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Optional, List, Union


class OpenScoreMasterGetSchema(BaseModel):
    pass


class OpenScoreShopGetSchema(BaseModel):
    pass


class OpenShopBrandPageGetSchema(BaseModel):
    pageNum: Optional[int] = Field(default=None, description="页码，首页为1")
    pageSize: Optional[int] = Field(default=None, description="单页请求数据量大小，最大为50")


class OpenShopEnterpriseQualificaitonExistSchema(BaseModel):
    metaDataInfo: Optional[dict] = Field(default=None, description="map的key默认传creditCode，value传社会统一信用码，社会信用码不传只会校验用户是不是有资质，不会与社会统一信用码比对")


class OpenShopInfoGetSchema(BaseModel):
    pass


class OpenShopPoiGetpoidetailbyouterpoiSchema(BaseModel):
    outerPoiId: Optional[str] = Field(default=None, description="图商poiId")
    source: Optional[int] = Field(default=None, description="图商来源：1-高德 2-百度 3-腾讯")
