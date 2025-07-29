# !/usr/bin/env python
# -*-coding:utf-8 -*-
from __future__ import annotations

import httpx

from ..exceptions import APIError
from ..models.common import APIWrapper
from ..models.document_center import *

_BASE = "/document-center/api/v1"


class DocumentCenterService:
    def __init__(self, http: httpx.Client):
        self._document = _Document(http)

    def get_documents(
            self, page_size: int = 9999, page_num: int = 1, name: str = ""
    ) -> List[Document]:
        return self._document.get_documents(page_size, page_num, name)

    @property
    def document(self) -> _Document:
        return self._document


class _Document:
    def __init__(self, http: httpx.Client):
        self._http = http

    def get_documents(
            self, page_size: int = 9999, page_num: int = 1, name: str = ""
    ) -> List[Document]:
        params = {"page_size": page_size, "page_num": page_num, "name": name}
        resp = self._http.get(f"{_BASE}/documents", params=params)
        if resp.status_code != 200:
            raise APIError(f"backend code {resp.status_code}: {resp.text}")
        res = resp.json()
        wrapper = APIWrapper[GetDocumentsResponse].model_validate(res)
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data.data
