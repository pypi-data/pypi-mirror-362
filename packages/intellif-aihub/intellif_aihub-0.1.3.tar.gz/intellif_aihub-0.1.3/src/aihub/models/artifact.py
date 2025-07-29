# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""制品管理模型模块

该模块定义了制品管理相关的数据模型，包括制品类型、创建制品请求、制品响应等。
"""
from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class ArtifactType(str, Enum):
    """制品类型枚举

    定义了系统支持的各种制品类型。
    """

    dataset = "dataset"  # 数据集类型
    model = "model"  # 模型类型
    metrics = "metrics"  # 指标类型
    log = "log"  # 日志类型
    checkpoint = "checkpoint"  # 检查点类型
    image = "image"  # 图像类型
    prediction = "prediction"  # 预测结果类型
    other = "other"  # 其他类型


class CreateArtifactsReq(BaseModel):
    """创建制品请求模型

    用于向服务器发送创建制品的请求。
    """

    entity_id: str
    """实体ID，通常是运行ID，用于关联制品与特定运行"""

    entity_type: ArtifactType = ArtifactType.other
    """制品类型，指定制品的类型，默认为other"""

    src_path: str
    """源路径，制品在系统中的路径标识"""

    is_dir: bool = False
    """是否为目录，True表示制品是一个目录，False表示是单个文件"""


class CreateArtifactsResponseData(BaseModel):
    """创建制品响应数据模型

    服务器创建制品后返回的数据。
    """

    id: int  # 制品ID
    s3_path: str  # S3存储路径


class CreateArtifactsResponseModel(BaseModel):
    """创建制品响应模型

    服务器对创建制品请求的完整响应。
    """

    code: int  # 响应码，0表示成功
    msg: str = ""  # 响应消息
    data: CreateArtifactsResponseData | None = None  # 响应数据


class CreatEvalReq(BaseModel):
    """创建评估请求模型

    用于创建模型评估的请求。
    """

    dataset_id: int  # 数据集ID
    dataset_version_id: int  # 数据集版本ID
    prediction_artifact_path: str  # 预测结果制品路径
    evaled_artifact_path: str  # 评估结果制品路径
    run_id: str  # 运行ID
    user_id: int  # 用户ID
    report: dict = {}  # 评估报告


class ArtifactResp(BaseModel):
    """制品响应模型

    表示一个制品的详细信息。
    """

    id: int  # 制品ID
    entity_type: str  # 实体类型
    entity_id: str  # 实体ID
    src_path: str  # 源路径
    s3_path: str  # S3存储路径
    is_dir: bool  # 是否为目录


class ArtifactRespData(BaseModel):
    """制品响应数据模型

    包含分页信息和制品列表的响应数据。
    """

    total: int  # 总记录数
    page_size: int  # 每页大小
    page_num: int  # 页码
    data: List[ArtifactResp]  # 制品列表


class ArtifactRespModel(BaseModel):
    """制品响应模型

    服务器对获取制品请求的完整响应。
    """

    code: int  # 响应码，0表示成功
    msg: str = ""  # 响应消息
    data: ArtifactRespData  # 响应数据


# 无限大的页面大小，用于一次性获取所有制品
InfinityPageSize = 10000 * 100


class StsResp(BaseModel):
    """STS临时凭证响应模型

    包含访问S3存储所需的临时凭证信息。
    """

    access_key_id: Optional[str] = None  # 访问密钥ID
    secret_access_key: Optional[str] = None  # 秘密访问密钥
    session_token: Optional[str] = None  # 会话令牌
    expiration: Optional[int] = None  # 过期时间
    endpoint: Optional[str] = None  # 端点URL
