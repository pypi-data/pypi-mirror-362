from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Env(BaseModel):
    key: str
    value: str


class Mount(BaseModel):
    name: str
    path: str


class Sku(BaseModel):
    cpu: int
    gpu: int
    memory: int


class VirtualCluster(BaseModel):
    id: int
    name: str
    gpu_type: str = Field(alias="gpu_type")
    label: str
    sku: Sku


class Storage(BaseModel):
    id: int
    name: str
    path: str
    server_path: str = Field(alias="server_path")
    server_host: str = Field(alias="server_host")
    server_type: str = Field(alias="server_type")
    permission: str
    description: str


class Category(BaseModel):
    id: int
    name: str


class Project(BaseModel):
    id: int
    name: str
    description: str


class User(BaseModel):
    id: int
    name: str


class Department(BaseModel):
    id: int
    name: str


class CreateTrainingRequest(BaseModel):
    framework: str
    name: str
    description: Optional[str] = None
    command: Optional[str] = None
    image: str
    virtual_cluster_id: int = Field(alias="virtual_cluster_id")
    sku_cnt: int = Field(alias="sku_cnt")
    enable_ssh: Optional[bool] = Field(False, alias="enable_ssh")
    envs: Optional[List[Env]] = Field(default_factory=list, alias="envs")
    storage_ids: Optional[List[int]] = Field(default_factory=list, alias="storage_ids")
    instances: int
    use_ib_network: Optional[bool] = Field(False, alias="use_ib_network")
    always_pull_image: Optional[bool] = Field(False, alias="always_pull_image")
    shm: Optional[int] = None
    category_id: int = Field(alias="category_id")
    project_id: int = Field(alias="project_id")
    estimate_run_time: Optional[int] = Field(None, alias="estimate_run_time")
    is_vip: Optional[bool] = Field(False, alias="is_vip")
    preempt_policy: Optional[int] = Field(None, alias="preempt_policy")
    vip_node_names: Optional[List[str]] = Field(default_factory=list, alias="vip_node_names")
    is_quota_schedule: Optional[bool] = Field(False, alias="is_quota_schedule")


class CreateTrainingResponse(BaseModel):
    id: int


class ListTrainingsRequest(BaseModel):
    page_size: int = Field(20, alias="page_size")
    page_num: int = Field(1, alias="page_num")
    user_id: Optional[int] = Field(None, alias="user_id")
    name: Optional[str] = None
    virtual_cluster_id: Optional[int] = Field(None, alias="virtual_cluster_id")
    status: Optional[int] = None
    category_id: Optional[int] = Field(None, alias="category_id")
    project_id: Optional[int] = Field(None, alias="project_id")
    is_quota_schedule: Optional[bool] = Field(None, alias="is_quota_schedule")


class Training(BaseModel):
    id: int
    framework: str
    name: str
    description: str
    command: str
    image: str
    virtual_cluster: VirtualCluster = Field(alias="virtual_cluster")
    sku_cnt: int = Field(alias="sku_cnt")
    enable_ssh: bool = Field(alias="enable_ssh")
    envs: Optional[List[Env]] = Field(None, alias="envs")
    storages: Optional[List[Storage]] = Field(None, alias="storages")
    instances: int
    created_at: int = Field(alias="created_at")
    username: str
    user_id: int = Field(alias="user_id")
    namespace: str
    res_name: str = Field(alias="res_name")
    status: int
    use_ib_network: bool = Field(alias="use_ib_network")
    always_pull_image: bool = Field(alias="always_pull_image")
    shm: int
    category: Category
    project: Project
    avg_gpu_util: float = Field(alias="avg_gpu_util")
    finished_at: int = Field(alias="finished_at")
    started_at: int = Field(alias="started_at")
    estimate_run_time: int = Field(alias="estimate_run_time")
    is_vip: bool = Field(alias="is_vip")
    cluster_partition: str = Field(alias="cluster_partition")
    preempt_policy: int = Field(alias="preempt_policy")
    vip_node_names: List[str] = Field(alias="vip_node_names")
    stop_op_user: Optional[User] = Field(None, alias="stop_op_user")
    use_new_log: bool = Field(alias="use_new_log")
    is_quota_schedule: bool = Field(alias="is_quota_schedule")


class ListTrainingsResponse(BaseModel):
    total: int
    page_size: int = Field(alias="page_size")
    page_num: int = Field(alias="page_num")
    data: List[Training]


class Pod(BaseModel):
    id: int
    namespace: str
    name: str
    status: str
    created_at: int = Field(alias="created_at")
    started_at: int = Field(alias="started_at")
    finished_at: int = Field(alias="finished_at")
    host_ip: str = Field(alias="host_ip")
    node_name: str = Field(alias="node_name")
    ssh_port: int = Field(alias="ssh_port")
    ssh_info: str = Field(alias="ssh_info")
    use_new_log: bool = Field(alias="use_new_log")


class ListTrainingPodsRequest(BaseModel):
    page_size: int = Field(20, alias="page_size")
    page_num: int = Field(1, alias="page_num")


class ListTrainingPodsResponse(BaseModel):
    total: int
    page_size: int = Field(alias="page_size")
    page_num: int = Field(alias="page_num")
    data: List[Pod]


class PodLogInfo(BaseModel):
    name: str
    url: str


class GetTrainingPodLogsNewResponse(BaseModel):
    logs: List[PodLogInfo]


class GetTrainingPodSpecResponse(BaseModel):
    spec: str


class GetTrainingPodEventsResponse(BaseModel):
    events: str


class TrainingUser(BaseModel):
    user_id: int = Field(alias="user_id")
    username: str


class ListTrainingUsersRequest(BaseModel):
    page_size: int = Field(20, alias="page_size")
    page_num: int = Field(1, alias="page_num")


class ListTrainingUsersResponse(BaseModel):
    total: int
    page_size: int = Field(alias="page_size")
    page_num: int = Field(alias="page_num")
    data: Optional[List[TrainingUser]] = Field(default_factory=list)


class Container(BaseModel):
    namespace: str
    pod_name: str = Field(alias="pod_name")
    container_name: str = Field(alias="container_name")


class TrainingContainer(BaseModel):
    training_id: int = Field(alias="training_id")
    training_name: str = Field(alias="training_name")
    containers: List[Container]


class ListTrainingContainersRequest(BaseModel):
    page_size: int = Field(20, alias="page_size")
    page_num: int = Field(1, alias="page_num")


class ListTrainingContainersResponse(BaseModel):
    total: int
    page_size: int = Field(alias="page_size")
    page_num: int = Field(alias="page_num")
    data: Optional[List[TrainingContainer]] = Field(default_factory=list)
