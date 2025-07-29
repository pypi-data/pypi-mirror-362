# !/usr/bin/env python
# -*-coding:utf-8 -*-

from __future__ import annotations

from typing import List, Optional, Any

from pydantic import BaseModel


class Document(BaseModel):
    id: int
    title: str
    type: int
    edit_time: int
    need_update: bool
    content: str
    username: str
    user_id: int
    created_at: int
    comments: Optional[Any] = None


class GetDocumentsResponse(BaseModel):
    total: int
    page_size: int
    page_num: int
    data: List[Document]
