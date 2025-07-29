from __future__ import annotations

import json
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field, field_serializer, field_validator


class TaskCenterPriorityEnum(Enum):
    """
    任务优先级枚举
    """

    low = "low"
    medium = "medium"
    high = "high"


class LabelProjectTypeEnum(Enum):
    """
    任务类型枚举
     1 - 目标检测 2 - 语义分割 3 - 图片分类 4 - 实例分割 5 - 视频标注 6 - 人类偏好文本标注 7- 敏感预料文本标注 8 - 文本标注 9 - 关键点标注
    """

    OBJECT_DETECTION = 1
    SEGMENTATION = 2
    IMAGE_CLASSIFICATION = 3
    INSTANCE_SEGMENTATION = 4
    VIDEO_LABELING = 5
    HUMAN_PREFERENCE_TEXT_LABELING = 6
    SENSITIVE_TEXT_LABELING = 7
    TEXT_LABELING = 8
    KEYPOINT_LABELING = 9


class CreateTaskOtherInfo(BaseModel):
    label_project_type: LabelProjectTypeEnum = LabelProjectTypeEnum.IMAGE_CLASSIFICATION
    dataset_id: int = Field(alias="dataset_id")
    dataset_version_id: int = Field(alias="dataset_version_id")
    doc_id: int = Field(alias="doc_id")
    doc_type: str = Field(alias="doc_type", default="doc_center")


class ProjectInfo(BaseModel):
    label_project_id: int = Field(alias="label_project_id")
    label_project_name: str = Field(alias="label_project_name")


class TaskDetailOtherInfo(BaseModel):
    label_project_type: LabelProjectTypeEnum = LabelProjectTypeEnum.IMAGE_CLASSIFICATION
    dataset_id: int = Field(alias="dataset_id")
    dataset_version_id: int = Field(alias="dataset_version_id")
    doc_id: int = Field(alias="doc_id")
    doc_type: str = Field(alias="doc_type", default="doc_center")
    label_projects: Optional[List[ProjectInfo]] = Field(alias="label_projects")


class CreateTaskReq(BaseModel):
    name: str
    description: Optional[str] = None
    task_priority: Optional[str] = None
    type: Optional[str] = None
    receiver_id: Optional[int] = None
    project_id: Optional[int] = None
    other_info: CreateTaskOtherInfo = Field(alias="other_info")
    estimated_delivery_at: Optional[int] = None

    @field_serializer("other_info")
    def serialize_other_info(self, value: CreateTaskOtherInfo) -> str:
        """将 other_info 序列化为 JSON 字符串"""
        return value.model_dump_json()


class CreateTaskResp(BaseModel):
    id: int = Field(alias="id")


class LabelTaskDetail(BaseModel):
    """任务详情"""

    name: str
    description: Optional[str] = Field(alias="description")
    task_priority: Optional[str] = Field(alias="task_priority")
    type: Optional[str] = Field(alias="type")
    receiver_id: Optional[int] = Field(alias="receiver_id")
    project_id: Optional[int] = None
    other_info: TaskDetailOtherInfo = Field(alias="other_info")
    estimated_delivery_at: Optional[int] = None

    @field_serializer("other_info")
    def serialize_other_info(self, value: TaskDetailOtherInfo) -> str:
        """将 other_info 序列化为 JSON 字符串"""
        return value.model_dump_json()

    @field_validator("other_info", mode="before")
    @classmethod
    def parse_other_info(cls, value):
        """将字符串解析为 TaskDetailOtherInfo 对象"""
        if isinstance(value, str):
            try:
                # 解析 JSON 字符串为字典
                data = json.loads(value)
                # 创建 TaskDetailOtherInfo 对象
                return TaskDetailOtherInfo(**data)
            except (json.JSONDecodeError, TypeError, ValueError) as e:
                raise ValueError(f"无法解析 other_info 字符串: {e}")
        elif isinstance(value, dict):
            # 如果传入的是字典，直接创建对象
            return TaskDetailOtherInfo(**value)
        elif isinstance(value, TaskDetailOtherInfo):
            # 如果已经是对象，直接返回
            return value
        else:
            raise ValueError(
                f"other_info 必须是字符串、字典或 TaskDetailOtherInfo 对象，得到: {type(value)}"
            )
