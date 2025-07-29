from __future__ import annotations

import os

import httpx

from .exceptions import APIError
from .services import artifact
from .services import dataset_management
from .services import document_center
from .services import labelfree
from .services import model_training_platform
from .services import tag_resource_management
from .services import task_center
from .services import user_system
from .services.artifact import ArtifactService
from .services.dataset_management import DatasetManagementService
from .services.document_center import DocumentCenterService
from .services.labelfree import LabelfreeService
from .services.model_training_platform import ModelTrainingPlatformService
from .services.tag_resource_management import TagResourceManagementService
from .services.task_center import TaskCenterService
from .services.user_system import UserSystemService


class Client:
    """AI-HUB python SDK 客户端

    Attributes:
        dataset_management (DatasetManagementService): 数据集管理服务
        labelfree (LabelfreeService): 标注服务
        task_center (TaskCenterService): 任务中心
        artifact (ArtifactService): 制品管理

    """

    labelfree: LabelfreeService = None
    tag_resource_management: TagResourceManagementService = None
    document_center: DocumentCenterService = None
    task_center: TaskCenterService = None
    dataset_management: DatasetManagementService = None
    artifact: ArtifactService = None
    user_system: UserSystemService = None
    model_training_platform: ModelTrainingPlatformService = None

    def __init__(self, *, base_url: str, token: str | None = None, timeout: float = 60.0):
        """AI-HUB python SDK 客户端

        Args:
            base_url (str): 服务地址
            token (str): 密钥，显式传入，或在环境变量AI_HUB_TOKEN中设置

        Examples:
            >>> from aihub.client import Client
            >>> client = Client(base_url="xxx", token="xxxx")

        """
        if not base_url:
            raise ValueError("base_url必须填写")

        token = os.getenv("AI_HUB_TOKEN") or token
        if not token:
            raise ValueError("缺少token：请显式传入，或在环境变量AI_HUB_TOKEN中设置")

        self._http = httpx.Client(
            base_url=base_url.rstrip("/"),
            timeout=timeout,
            headers={"Authorization": f"Bearer {token}"},
            # event_hooks={"response": [self._raise_for_status]},
        )
        self.dataset_management = dataset_management.DatasetManagementService(self._http)
        self.labelfree = labelfree.LabelfreeService(self._http)
        self.tag_resource_management = tag_resource_management.TagResourceManagementService(self._http)
        self.document_center = document_center.DocumentCenterService(self._http)
        self.task_center = task_center.TaskCenterService(self._http)
        self.artifact = artifact.ArtifactService(self._http)
        self.user_system = user_system.UserSystemService(self._http)
        self.model_training_platform = model_training_platform.ModelTrainingPlatformService(self._http)

    @staticmethod
    def _raise_for_status(r: httpx.Response):
        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise APIError(f"{e.response.status_code}: {e.response.text}") from e

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self._http.close()
