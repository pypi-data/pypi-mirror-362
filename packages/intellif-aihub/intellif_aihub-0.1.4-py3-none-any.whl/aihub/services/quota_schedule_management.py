from __future__ import annotations

import os
from pathlib import Path

import httpx

from ..exceptions import APIError
from ..models.common import APIWrapper
from ..models.quota_schedule_management import *

_ENV_KEY = "PRE_STOP_SENTINEL_FILE"
_DEFAULT_SENTINEL = "/tmp/pre_stop_sentinel_file"
_SENTINEL_PATH = Path(os.getenv(_ENV_KEY, _DEFAULT_SENTINEL))
_BASE = "/quota-schedule-management/api/v1"


def is_pre_stopped() -> bool:
    return _SENTINEL_PATH.exists()


class PreStopService:
    @staticmethod
    def is_pre_stopped() -> bool:
        return is_pre_stopped()


class QuotaScheduleManagementService:

    def __init__(self, http: httpx.Client):
        self._task = _Task(http)

    def create_task(self, payload: CreateTaskRequest) -> int:
        """创建调度任务

        Args:
            payload: 创建任务的各项参数

        Returns:
            int: 后端生成的任务 ID
        """
        return self._task.create(payload)

    def list_tasks(self, payload: ListTasksRequest) -> ListTasksResponse:
        """分页查询任务列表

        Args:
            payload: 查询条件（分页 / 过滤）

        Returns:
            ListTasksResponse: 列表及分页信息
        """
        return self._task.list(payload)

    def get_task(self, task_id: int) -> Task:
        """获取任务详情

        Args:
            task_id: 任务 ID

        Returns:
            Task: 任务完整信息
        """
        return self._task.get(task_id)

    def stop_task(self, task_id: int) -> None:
        """停止任务

        Args:
            task_id: 任务 ID

        Returns:
            None
        """
        self._task.stop(task_id)

    def list_task_pods(self, task_id: int, payload: ListTaskPodsRequest) -> ListTaskPodsResponse:
        return self._task.list_pods(task_id, payload)

    def get_task_pod(self, task_id: int, pod_id: int) -> Pod:
        return self._task.get_pod(task_id, pod_id)

    def get_pod_logs_new(self, task_id: int, pod_id: int) -> List[PodLogInfo]:
        return self._task.get_logs_new(task_id, pod_id).logs

    def get_pod_spec(self, task_id: int, pod_id: int) -> str:
        return self._task.get_spec(task_id, pod_id).spec

    def get_pod_events(self, task_id: int, pod_id: int) -> str:
        return self._task.get_events(task_id, pod_id).events

    def list_task_users(self, payload: ListTaskUsersRequest) -> ListTaskUsersResponse:
        return self._task.list_users(payload)

    def get_metrics_overview(self, payload: GetMetricsOverviewRequest) -> GetMetricsOverviewResponse:
        return self._task.get_metrics_overview(payload)

    @property
    def task(self) -> _Task:
        return self._task


class _Task:

    def __init__(self, http: httpx.Client):
        self._http = http

    def create(self, payload: CreateTaskRequest) -> int:
        resp = self._http.post(f"{_BASE}/tasks", json=payload.model_dump(by_alias=True, exclude_none=True))
        wrapper = APIWrapper[CreateTaskResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data.id

    def list(self, payload: ListTasksRequest) -> ListTasksResponse:
        resp = self._http.get(f"{_BASE}/tasks", params=payload.model_dump(by_alias=True, exclude_none=True))
        wrapper = APIWrapper[ListTasksResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def get(self, task_id: int) -> Task:
        resp = self._http.get(f"{_BASE}/tasks/{task_id}")
        wrapper = APIWrapper[Task].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def stop(self, task_id: int) -> None:
        resp = self._http.post(f"{_BASE}/tasks/{task_id}/stop")
        wrapper = APIWrapper[dict].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")

    def list_pods(self, task_id: int, payload: ListTaskPodsRequest) -> ListTaskPodsResponse:
        resp = self._http.get(f"{_BASE}/tasks/{task_id}/pods", params=payload.model_dump(by_alias=True))
        wrapper = APIWrapper[ListTaskPodsResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def get_pod(self, task_id: int, pod_id: int) -> Pod:
        resp = self._http.get(f"{_BASE}/tasks/{task_id}/pods/{pod_id}")
        wrapper = APIWrapper[Pod].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def get_logs_new(self, task_id: int, pod_id: int) -> GetTaskPodLogsNewResponse:
        resp = self._http.get(f"{_BASE}/tasks/{task_id}/pods/{pod_id}/logs/new")
        wrapper = APIWrapper[GetTaskPodLogsNewResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def get_spec(self, task_id: int, pod_id: int) -> GetTaskPodSpecResponse:
        resp = self._http.get(f"{_BASE}/tasks/{task_id}/pods/{pod_id}/spec")
        wrapper = APIWrapper[GetTaskPodSpecResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def get_events(self, task_id: int, pod_id: int) -> GetTaskPodEventsResponse:
        resp = self._http.get(f"{_BASE}/tasks/{task_id}/pods/{pod_id}/events")
        wrapper = APIWrapper[GetTaskPodEventsResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def list_users(self, payload: ListTaskUsersRequest) -> ListTaskUsersResponse:
        resp = self._http.get(f"{_BASE}/task-users", params=payload.model_dump(by_alias=True))
        wrapper = APIWrapper[ListTaskUsersResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def get_metrics_overview(self, payload: GetMetricsOverviewRequest) -> GetMetricsOverviewResponse:
        resp = self._http.get(f"{_BASE}/metrics/overview", params=payload.model_dump(by_alias=True))
        wrapper = APIWrapper[GetMetricsOverviewResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data
