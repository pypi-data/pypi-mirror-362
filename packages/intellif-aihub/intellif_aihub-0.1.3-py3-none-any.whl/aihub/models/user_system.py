# !/usr/bin/env python
# -*-coding:utf-8 -*-
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


# ======================================================================
# COMMON
# ======================================================================

class Role(BaseModel):
    id: int
    name: str
    role_type: int = Field(alias="role_type")
    menu_ids: Optional[List[int]] = Field(None, alias="menu_ids")


class Menu(BaseModel):
    id: int
    name: str
    parent: int
    auth: str


class TreeMenu(BaseModel):
    id: int
    name: str
    parent: int
    auth: str
    children: Optional[List["TreeMenu"]] = None
    roles: Optional[List[Role]] = None


class TagBrief(BaseModel):
    id: int
    name: str


# ======================================================================
# ------------------------------- AUTH ---------------------------------
# ======================================================================

class LoginRequest(BaseModel):
    username: str = Field(alias="username")
    password: str = Field(alias="password")


class LoginResponse(BaseModel):
    id: int = Field(alias="id")
    token: str = Field(alias="token")


class SignupRequest(BaseModel):
    username: str = Field(alias="username")
    password: str = Field(alias="password")
    nickname: str = Field(alias="nickname")
    email: str = Field(alias="email")
    role_ids: List[int] = Field(alias="role_ids")


class SignupResponse(BaseModel):
    id: int = Field(alias="id")


# ======================================================================
# ------------------------------- MENU ---------------------------------
# ======================================================================
class ListMenusRequest(BaseModel):
    need_roles: Optional[bool] = Field(None, alias="need_roles")


class ListMenusResponse(BaseModel):
    menus: List[TreeMenu] = Field(None, alias="menus")


class CreateMenuRequest(BaseModel):
    name: str = Field(alias="name")
    parent: int = Field(alias="parent")
    auth: str = Field(alias="auth")
    role_ids: Optional[List[int]] = Field(None, alias="role_ids")


class CreateMenuResponse(BaseModel):
    id: int = Field(alias="id")


class UpdateMenuRequest(BaseModel):
    name: Optional[str] = Field(None, alias="name")
    parent: Optional[int] = Field(None, alias="parent")
    auth: str = Field(alias="auth")
    role_ids: Optional[List[int]] = Field(None, alias="role_ids")


class GetMenuRolesResponse(BaseModel):
    role_ids: List[int] = Field(alias="role_ids")


class SetMenuRolesRequest(BaseModel):
    role_ids: List[int] = Field(alias="role_ids")


class SearchMenusRequest(BaseModel):
    page_size: int = Field(20, alias="page_size")
    page_num: int = Field(1, alias="page_num")
    name: Optional[str] = None
    parent_ids: Optional[List[int]] = Field(None, alias="parent_ids")
    auth: Optional[str] = None
    menu_ids: Optional[List[int]] = Field(None, alias="menu_ids")


class SearchMenusResponse(BaseModel):
    total: int
    page_size: int = Field(alias="page_size")
    page_num: int = Field(alias="page_num")
    data: List[Menu]


# ======================================================================
# ------------------------------- ROLE ---------------------------------
# ======================================================================


class CreateRoleRequest(BaseModel):
    id: Optional[int] = Field(None, alias="id")
    name: str
    role_type: int = Field(alias="role_type")
    menu_ids: Optional[List[int]] = Field(None, alias="menu_ids")


class CreateRoleResponse(BaseModel):
    id: int


class UpdateRoleRequest(BaseModel):
    name: Optional[str] = None
    role_type: Optional[int] = Field(None, alias="role_type")
    menu_ids: Optional[List[int]] = Field(None, alias="menu_ids")


class GetRoleMenusResponse(BaseModel):
    menu_ids: List[int] = Field(alias="menu_ids")


class SetRoleMenusRequest(BaseModel):
    menu_ids: List[int] = Field(alias="menu_ids")


class ListRolesRequest(BaseModel):
    page_size: int = Field(20, alias="page_size")
    page_num: int = Field(1, alias="page_num")
    role_type: Optional[int] = Field(None, alias="role_type")


class ListRolesResponse(BaseModel):
    total: int
    page_size: int = Field(alias="page_size")
    page_num: int = Field(alias="page_num")
    data: List[Role]


class SearchRolesRequest(BaseModel):
    page_size: int = Field(20, alias="page_size")
    page_num: int = Field(1, alias="page_num")
    name: Optional[str] = None
    role_ids: Optional[List[int]] = Field(None, alias="role_ids")
    menu_ids: Optional[List[int]] = Field(None, alias="menu_ids")


class SearchRolesResponse(BaseModel):
    total: int
    page_size: int = Field(alias="page_size")
    page_num: int = Field(alias="page_num")
    data: List[Role]


# ======================================================================
# ------------------------------- USER ---------------------------------
# ======================================================================

class User(BaseModel):
    id: int
    username: str
    nickname: str
    email: str
    roles: Optional[List[Role]] = Field(None, alias="roles")
    status: int
    tags: Optional[List[TagBrief]] = Field(None, alias="tags")
    created_at: int = Field(alias="created_at")


class ListUsersRequest(BaseModel):
    page_size: int = Field(20, alias="page_size")
    page_num: int = Field(1, alias="page_num")
    search_key: Optional[str] = Field(None, alias="search_key")


class ListUsersResponse(BaseModel):
    total: int
    page_size: int = Field(alias="page_size")
    page_num: int = Field(alias="page_num")
    data: List[User]


class CreateUserRequest(BaseModel):
    id: int
    username: str
    password: str
    nickname: str
    email: str
    role_ids: Optional[List[int]] = Field(None, alias="role_ids")
    created_at: Optional[int] = Field(None, alias="created_at")
    updated_at: Optional[int] = Field(None, alias="updated_at")
    status: Optional[int] = None
    tag_ids: Optional[List[int]] = Field(None, alias="tag_ids")


class CreateUserResponse(BaseModel):
    id: int


class UpdateUserRequest(BaseModel):
    username: Optional[str] = None
    nickname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role_ids: Optional[List[int]] = Field(default_factory=list, alias="role_ids")
    status: Optional[int] = None
    tag_ids: Optional[List[int]] = Field(default_factory=list, alias="tag_ids")


class SetUserRolesRequest(BaseModel):
    role_ids: List[int] = Field(alias="role_ids")


class GetUserMenusResponse(BaseModel):
    menus: List[TreeMenu]


class SearchUsersRequest(BaseModel):
    page_size: int = Field(20, alias="page_size")
    page_num: int = Field(1, alias="page_num")
    username: Optional[str] = None
    nickname: Optional[str] = None
    email: Optional[str] = None
    user_ids: Optional[List[int]] = Field(None, alias="user_ids")
    role_ids: Optional[List[int]] = Field(None, alias="role_ids")
    role_names: Optional[List[str]] = Field(None, alias="role_names")
    status: Optional[int] = None


class SearchUsersResponse(BaseModel):
    total: int
    page_size: int = Field(alias="page_size")
    page_num: int = Field(alias="page_num")
    data: List[User]


# 此行放在文件末尾，否则序列化报错
TreeMenu.update_forward_refs()
