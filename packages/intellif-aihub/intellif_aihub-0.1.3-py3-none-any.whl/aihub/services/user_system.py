# !/usr/bin/env python
# -*-coding:utf-8 -*-
from __future__ import annotations

import httpx

from ..exceptions import APIError
from ..models.common import APIWrapper
from ..models.user_system import *


class UserSystemService:

    def __init__(self, http: httpx.Client):
        self._auth = _Auth(http)
        self._menu = _Menu(http)
        self._role = _Role(http)
        self._user = _User(http)

    # ==================================================
    #  AUTH 一级方法
    # ==================================================
    def login(self, payload: LoginRequest) -> LoginResponse:
        return self._auth.login(payload)

    def signup(self, payload: SignupRequest) -> SignupResponse:
        return self._auth.signup(payload)

    # ==================================================
    #  MENU 一级方法
    # ==================================================
    def list_menus(self, need_roles: bool = False) -> ListMenusResponse:
        return self._menu.list(need_roles)

    def get_menu(self, menu_id: int) -> Menu:
        return self._menu.get(menu_id)

    def create_menu(self, payload: CreateMenuRequest) -> int:
        return self._menu.create(payload)

    def update_menu(self, menu_id: int, payload: UpdateMenuRequest) -> None:
        self._menu.update(menu_id, payload)

    def delete_menu(self, menu_id: int) -> None:
        self._menu.delete(menu_id)

    def get_menu_roles(self, menu_id: int) -> List[int]:
        return self._menu.get_roles(menu_id)

    def set_menu_roles(self, menu_id: int, role_ids: List[int]) -> None:
        self._menu.set_roles(menu_id, role_ids)

    # ==================================================
    #  ROLE 一级方法
    # ==================================================
    def list_roles(self, payload: ListRolesRequest) -> ListRolesResponse:
        return self._role.list(payload)

    def get_role(self, role_id: int) -> Role:
        return self._role.get(role_id)

    def create_role(self, payload: CreateRoleRequest) -> int:
        return self._role.create(payload)

    def update_role(self, role_id: int, payload: UpdateRoleRequest) -> None:
        self._role.update(role_id, payload)

    def delete_role(self, role_id: int) -> None:
        self._role.delete(role_id)

    def get_role_menus(self, role_id: int) -> List[int]:
        return self._role.get_menus(role_id)

    def set_role_menus(self, role_id: int, menu_ids: List[int]) -> None:
        self._role.set_menus(role_id, menu_ids)

    def search_roles(self, payload: SearchRolesRequest) -> SearchRolesResponse:
        return self._role.search(payload)

    # ==================================================
    #  USER 一级方法
    # ==================================================
    def list_users(self, payload: ListUsersRequest) -> ListUsersResponse:
        return self._user.list(payload)

    def get_user(self, user_id: int) -> User:
        return self._user.get(user_id)

    def create_user(self, payload: CreateUserRequest) -> int:
        return self._user.create(payload)

    def update_user(self, user_id: int, payload: UpdateUserRequest) -> None:
        self._user.update(user_id, payload)

    def delete_user(self, user_id: int) -> None:
        self._user.delete(user_id)

    def set_user_roles(self, user_id: int, payload: SetUserRolesRequest) -> None:
        self._user.set_roles(user_id, payload)

    def get_user_menus(self, user_id: int, parent_id: int | None = None, auth: str | None = None, ) -> List[TreeMenu]:
        return self._user.get_menus(user_id, parent_id=parent_id, auth=auth)

    def search_users(self, payload: SearchUsersRequest) -> SearchUsersResponse:
        return self._user.search(payload)

    def search_one(self, payload: SearchUsersRequest) -> int:
        return self._user.search_one(payload)

    @property
    def auth(self) -> _Auth:
        return self._auth

    @property
    def menu(self) -> _Menu:
        return self._menu

    @property
    def role(self) -> _Role:
        return self._role

    @property
    def user(self) -> _User:
        return self._user


class _Auth:
    _base = "/api/v1/auth"

    def __init__(self, http: httpx.Client):
        self._http = http

    def login(self, req: LoginRequest) -> LoginResponse:
        resp = self._http.post(
            f"{self._base}/login",
            json=req.model_dump(by_alias=True, exclude_none=True),
        )
        wrapper = APIWrapper[LoginResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def signup(self, req: SignupRequest) -> SignupResponse:
        resp = self._http.post(
            f"{self._base}/signup",
            json=req.model_dump(by_alias=True, exclude_none=True),
        )
        wrapper = APIWrapper[SignupResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data


class _Menu:
    _base = "/api/v1/menus"

    def __init__(self, http: httpx.Client):
        self._http = http

    def list(self, need_roles: bool) -> ListMenusResponse:
        resp = self._http.get(self._base, params={"need_roles": str(need_roles).lower()})
        wrapper = APIWrapper[ListMenusResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def get(self, menu_id: int) -> Menu:
        resp = self._http.get(f"{self._base}/{menu_id}")
        wrapper = APIWrapper[Menu].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def create(self, req: CreateMenuRequest) -> int:
        resp = self._http.post(self._base, json=req.model_dump(by_alias=True, exclude_none=True))
        wrapper = APIWrapper[CreateMenuResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data.id

    def update(self, menu_id: int, req: UpdateMenuRequest) -> None:
        resp = self._http.put(f"{self._base}/{menu_id}", json=req.model_dump(by_alias=True, exclude_none=True))
        wrapper = APIWrapper[dict].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")

    def delete(self, menu_id: int) -> None:
        resp = self._http.delete(f"{self._base}/{menu_id}")
        wrapper = APIWrapper[dict].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")

    def get_roles(self, menu_id: int) -> List[int]:
        resp = self._http.get(f"{self._base}/{menu_id}/roles")
        wrapper = APIWrapper[GetMenuRolesResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data.role_ids

    def set_roles(self, menu_id: int, role_ids: List[int]) -> None:
        resp = self._http.put(f"{self._base}/{menu_id}/roles", json={"role_ids": role_ids})
        wrapper = APIWrapper[dict].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")


class _Role:
    _base = "/api/v1/roles"
    _search = "/api/v1/search-roles"

    def __init__(self, http: httpx.Client):
        self._http = http

    def list(self, req: ListRolesRequest) -> ListRolesResponse:
        resp = self._http.get(self._base, params=req.model_dump(by_alias=True, exclude_none=True))
        wrapper = APIWrapper[ListRolesResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def get(self, role_id: int) -> Role:
        resp = self._http.get(f"{self._base}/{role_id}")
        wrapper = APIWrapper[Role].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def create(self, req: CreateRoleRequest) -> int:
        resp = self._http.post(self._base, json=req.model_dump(by_alias=True, exclude_none=True))
        wrapper = APIWrapper[CreateRoleResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data.id

    def update(self, role_id: int, req: UpdateRoleRequest) -> None:
        resp = self._http.put(f"{self._base}/{role_id}", json=req.model_dump(by_alias=True, exclude_none=True))
        wrapper = APIWrapper[dict].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")

    def delete(self, role_id: int) -> None:
        resp = self._http.delete(f"{self._base}/{role_id}")
        wrapper = APIWrapper[dict].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")

    def get_menus(self, role_id: int) -> List[int]:
        resp = self._http.get(f"{self._base}/{role_id}/menus")
        wrapper = APIWrapper[GetRoleMenusResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data.menu_ids

    def set_menus(self, role_id: int, menu_ids: List[int]) -> None:
        resp = self._http.put(f"{self._base}/{role_id}/menus", json={"menu_ids": menu_ids})
        wrapper = APIWrapper[dict].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")

    def search(self, req: SearchRolesRequest) -> SearchRolesResponse:
        resp = self._http.post(self._search, json=req.model_dump(by_alias=True, exclude_none=True))
        wrapper = APIWrapper[SearchRolesResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data


class _User:
    _base = "/api/v1/users"
    _search = "/api/v1/search-users"

    def __init__(self, http: httpx.Client):
        self._http = http

    def list(self, req: ListUsersRequest) -> ListUsersResponse:
        resp = self._http.get(self._base, params=req.model_dump(by_alias=True, exclude_none=True))
        wrapper = APIWrapper[ListUsersResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def get(self, user_id: int) -> User:
        resp = self._http.get(f"{self._base}/{user_id}")
        wrapper = APIWrapper[User].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def create(self, req: CreateUserRequest) -> int:
        resp = self._http.post(self._base, json=req.model_dump(by_alias=True, exclude_none=True))
        wrapper = APIWrapper[CreateUserResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data.id

    def update(self, user_id: int, req: UpdateUserRequest) -> None:
        resp = self._http.put(f"{self._base}/{user_id}", json=req.model_dump(by_alias=True, exclude_none=True))
        wrapper = APIWrapper[dict].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")

    def delete(self, user_id: int) -> None:
        resp = self._http.delete(f"{self._base}/{user_id}")
        wrapper = APIWrapper[dict].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")

    def set_roles(self, user_id: int, req: SetUserRolesRequest) -> None:
        resp = self._http.put(f"{self._base}/{user_id}/roles", json=req.model_dump(by_alias=True, exclude_none=True))
        wrapper = APIWrapper[dict].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")

    def get_menus(self, user_id: int, parent_id: int | None = None, auth: str | None = None) -> List[TreeMenu]:
        params = {}
        if parent_id is not None:
            params["parent_id"] = parent_id
        if auth:
            params["auth"] = auth

        resp = self._http.get(f"{self._base}/{user_id}/menus", params=params)
        wrapper = APIWrapper[GetUserMenusResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data.menus

    def search(self, req: SearchUsersRequest) -> SearchUsersResponse:
        resp = self._http.post(self._search, json=req.model_dump(by_alias=True, exclude_none=True))
        wrapper = APIWrapper[SearchUsersResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def search_one(self, req: SearchUsersRequest) -> int:
        resp = self.search(req)
        for user in resp.data:
            if user.nickname == req.nickname:
                return user.id
        raise APIError("no user found")
