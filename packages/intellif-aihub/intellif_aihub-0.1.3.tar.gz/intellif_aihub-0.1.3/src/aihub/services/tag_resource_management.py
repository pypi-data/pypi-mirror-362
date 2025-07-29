# !/usr/bin/env python
# -*-coding:utf-8 -*-
from __future__ import annotations

import httpx

from ..exceptions import APIError
from ..models.common import APIWrapper
from ..models.tag_resource_management import *

_BASE = "/tag-resource-management/api/v1"


class TagResourceManagementService:
    def __init__(self, http: httpx.Client):
        self._project = _Project(http)
        self._virtual_cluster = _VirtualCluster(http)

    def select_projects(self) -> List[Project]:
        return self._project.select_projects()

    def select_virtual_clusters(self, payload: SelectVirtualClustersRequest) -> List[VirtualClusterBrief]:
        return self._virtual_cluster.select(payload).data

    @property
    def project(self) -> _Project:
        return self._project

    @property
    def virtual_cluster(self) -> _VirtualCluster:
        return self._virtual_cluster


class _Project:
    def __init__(self, http: httpx.Client):
        self._http = http

    def select_projects(self) -> List[Project]:
        resp = self._http.get(f"{_BASE}/select-projects")
        wrapper = APIWrapper[ProjectListData].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data.data


class _VirtualCluster:
    def __init__(self, http: httpx.Client):
        self._http = http

    def select(self, payload: SelectVirtualClustersRequest) -> SelectVirtualClustersResponse:
        resp = self._http.get(f"{_BASE}/select-clusters", params=payload.model_dump(by_alias=True, exclude_none=True))
        wrapper = APIWrapper[SelectVirtualClustersResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data
