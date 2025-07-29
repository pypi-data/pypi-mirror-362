# !/usr/bin/env python
# -*-coding:utf-8 -*-

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Project(BaseModel):
    id: int
    name: str


class ProjectListData(BaseModel):
    data: List[Project]


class SelectProjectsResponse(BaseModel):
    data: List[Project]


class SkuBrief(BaseModel):
    id: int
    description: str
    cpu: int
    memory: int
    gpu_type: int = Field(alias="gpu_type")
    gpu_memory: int = Field(alias="gpu_memory")
    network: int
    created_at: int = Field(alias="created_at")


class VirtualClusterBrief(BaseModel):
    id: int
    name: str
    uuid: str
    sku: Optional[SkuBrief] = None
    created_at: int = Field(alias="created_at")


class SelectVirtualClustersRequest(BaseModel):
    user_id: int = Field(alias="user_id")
    module_type: Optional[int] = Field(None, alias="module_type")
    new_module_type: Optional[str] = Field(None, alias="new_module_type")


class SelectVirtualClustersResponse(BaseModel):
    data: Optional[List[VirtualClusterBrief]] = Field(default_factory=list)
