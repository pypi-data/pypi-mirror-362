from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Env(BaseModel):
    key: str
    value: str


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


class SourceTask(BaseModel):
    id: int
    name: str


class CreateTaskRequest(BaseModel):
    priority: int
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
    enable_reschedule: Optional[bool] = Field(False, alias="enable_reschedule")


class CreateTaskResponse(BaseModel):
    id: int


class Task(BaseModel):
    id: int
    priority: int
    mtp_id: int = Field(alias="mtp_id")
    framework: str
    name: str
    description: str
    command: str
    image: str
    virtual_cluster: VirtualCluster = Field(alias="virtual_cluster")
    sku_cnt: int = Field(alias="sku_cnt")
    enable_ssh: bool = Field(alias="enable_ssh")
    envs: Optional[List[Env]] = Field(default_factory=list, alias="envs")
    storages: Optional[List[Storage]] = Field(default_factory=list, alias="storages")
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
    vip_node_names: Optional[List[str]] = Field(None, alias="vip_node_names")
    stop_op_user: Optional[User] = Field(None, alias="stop_op_user")
    use_new_log: bool = Field(alias="use_new_log")
    is_quota_schedule: bool = Field(alias="is_quota_schedule")
    enable_reschedule: bool = Field(alias="enable_reschedule")
    remain_schedule_cnt: int = Field(alias="remain_schedule_cnt")
    source_task: Optional[SourceTask] = Field(None, alias="source_task")


class ListTasksRequest(BaseModel):
    page_size: int = Field(20, alias="page_size")
    page_num: int = Field(1, alias="page_num")
    user_id: Optional[int] = Field(None, alias="user_id")
    name: Optional[str] = None
    virtual_cluster_id: Optional[int] = Field(None, alias="virtual_cluster_id")
    status: Optional[int] = None
    category_id: Optional[int] = Field(None, alias="category_id")
    project_id: Optional[int] = Field(None, alias="project_id")
    priority: Optional[int] = None


class ListTasksResponse(BaseModel):
    total: int
    page_size: int = Field(alias="page_size")
    page_num: int = Field(alias="page_num")
    data: List[Task] = Field(default_factory=list)


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


class ListTaskPodsRequest(BaseModel):
    page_size: int = Field(20, alias="page_size")
    page_num: int = Field(1, alias="page_num")


class ListTaskPodsResponse(BaseModel):
    total: int
    page_size: int = Field(alias="page_size")
    page_num: int = Field(alias="page_num")
    data: List[Pod] = Field(default_factory=list)


class PodLogInfo(BaseModel):
    name: str
    url: str


class GetTaskPodLogsNewResponse(BaseModel):
    logs: List[PodLogInfo]


class GetTaskPodSpecResponse(BaseModel):
    spec: str


class GetTaskPodEventsResponse(BaseModel):
    events: str


class MachineOverview(BaseModel):
    high: int
    low: int
    free: int


class HighPrioritySummary(BaseModel):
    group_id: int = Field(alias="group_id")
    group_name: str = Field(alias="group_name")
    used: int
    total: int


class MetricsOverview(BaseModel):
    vc_id: int = Field(alias="vc_id")
    vc_name: str = Field(alias="vc_name")
    machine: MachineOverview
    high_priority: List[HighPrioritySummary] = Field(alias="high_priority")


class GetMetricsOverviewRequest(BaseModel):
    page_size: int = Field(20, alias="page_size")
    page_num: int = Field(1, alias="page_num")


class GetMetricsOverviewResponse(BaseModel):
    total: int
    page_size: int = Field(alias="page_size")
    page_num: int = Field(alias="page_num")
    data: List[MetricsOverview] = Field(default_factory=list)


class TaskUser(BaseModel):
    user_id: int = Field(alias="user_id")
    username: str


class ListTaskUsersRequest(BaseModel):
    page_size: int = Field(20, alias="page_size")
    page_num: int = Field(1, alias="page_num")


class ListTaskUsersResponse(BaseModel):
    total: int
    page_size: int = Field(alias="page_size")
    page_num: int = Field(alias="page_num")
    data: List[TaskUser] = Field(default_factory=list)
