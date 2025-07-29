from __future__ import annotations

import httpx

from ..exceptions import APIError
from ..models.common import APIWrapper
from ..models.model_training_platform import *

_BASE = "/model-training-platform/api/v1"


class ModelTrainingPlatformService:

    def __init__(self, http: httpx.Client):
        self._training = _Training(http)

    def create_training(self, payload: CreateTrainingRequest) -> int:
        return self._training.create(payload)

    def list_trainings(self, payload: ListTrainingsRequest) -> ListTrainingsResponse:
        return self._training.list(payload)

    def get_training(self, training_id: int) -> Training:
        return self._training.get(training_id)

    def stop_training(self, training_id: int) -> None:
        self._training.stop(training_id)

    def list_training_pods(self, training_id: int, payload: ListTrainingPodsRequest) -> ListTrainingPodsResponse:
        return self._training.list_training_pods(training_id, payload)

    def get_training_pod(self, training_id: int, pod_id: int) -> Pod:
        return self._training.get_training_pod(training_id, pod_id)

    def get_pod_logs_new(self, training_id: int, pod_id: int) -> GetTrainingPodLogsNewResponse:
        return self._training.get_training_logs_new(training_id, pod_id)

    def get_pod_spec(self, training_id: int, pod_id: int) -> GetTrainingPodSpecResponse:
        return self._training.get_training_spec(training_id, pod_id)

    def get_pod_events(self, training_id: int, pod_id: int) -> GetTrainingPodEventsResponse:
        return self._training.get_training_events(training_id, pod_id)

    def list_training_users(self, payload: ListTrainingUsersRequest) -> ListTrainingUsersResponse:
        return self._training.list_training_users(payload)

    def list_training_containers(self, payload: ListTrainingContainersRequest) -> ListTrainingContainersResponse:
        return self._training.list_training_containers(payload)

    @property
    def training(self) -> _Training:
        return self._training


class _Training:

    def __init__(self, http: httpx.Client):
        self._http = http

    def create(self, payload: CreateTrainingRequest) -> int:
        resp = self._http.post(f"{_BASE}/trainings", json=payload.model_dump(by_alias=True, exclude_none=True))
        wrapper = APIWrapper[CreateTrainingResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data.id

    def list(self, payload: ListTrainingsRequest) -> ListTrainingsResponse:
        resp = self._http.get(f"{_BASE}/trainings", params=payload.model_dump(by_alias=True, exclude_none=True))
        wrapper = APIWrapper[ListTrainingsResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def get(self, training_id: int) -> Training:
        resp = self._http.get(f"{_BASE}/trainings/{training_id}")
        wrapper = APIWrapper[Training].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def stop(self, training_id: int) -> None:
        resp = self._http.post(f"{_BASE}/trainings/{training_id}/stop")
        wrapper = APIWrapper[dict].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")

    def list_training_pods(self, training_id: int, payload: ListTrainingPodsRequest) -> ListTrainingPodsResponse:
        resp = self._http.get(f"{_BASE}/trainings/{training_id}/pods",
                              params=payload.model_dump(by_alias=True, exclude_none=True))
        wrapper = APIWrapper[ListTrainingPodsResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def get_training_pod(self, training_id: int, pod_id: int) -> Pod:
        resp = self._http.get(f"{_BASE}/trainings/{training_id}/pods/{pod_id}")
        wrapper = APIWrapper[Pod].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def get_training_logs_new(self, training_id: int, pod_id: int) -> GetTrainingPodLogsNewResponse:
        resp = self._http.get(f"{_BASE}/trainings/{training_id}/pods/{pod_id}/logs/new")
        wrapper = APIWrapper[GetTrainingPodLogsNewResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def get_training_spec(self, training_id: int, pod_id: int) -> GetTrainingPodSpecResponse:
        resp = self._http.get(f"{_BASE}/trainings/{training_id}/pods/{pod_id}/spec")
        wrapper = APIWrapper[GetTrainingPodSpecResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def get_training_events(self, training_id: int, pod_id: int) -> GetTrainingPodEventsResponse:
        resp = self._http.get(f"{_BASE}/trainings/{training_id}/pods/{pod_id}/events")
        wrapper = APIWrapper[GetTrainingPodEventsResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def list_training_users(self, payload: ListTrainingUsersRequest) -> ListTrainingUsersResponse:
        resp = self._http.get(f"{_BASE}/training-users", params=payload.model_dump(by_alias=True))
        wrapper = APIWrapper[ListTrainingUsersResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def list_training_containers(self, payload: ListTrainingContainersRequest) -> ListTrainingContainersResponse:
        resp = self._http.get(f"{_BASE}/training-containers", params=payload.model_dump(by_alias=True))
        wrapper = APIWrapper[ListTrainingContainersResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data
