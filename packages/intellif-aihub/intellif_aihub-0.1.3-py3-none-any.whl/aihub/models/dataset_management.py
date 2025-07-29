from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class CreateDatasetRequest(BaseModel):
    name: str
    description: str
    tags: List[int]
    cover_img: Optional[str] = Field(None, alias="cover_img")
    create_by: Optional[int] = Field(None, alias="create_by")
    is_private: Optional[bool] = Field(None, alias="is_private")
    access_user_ids: Optional[List[int]] = Field(None, alias="access_user_ids")


class CreateDatasetResponse(BaseModel):
    id: int = Field(alias="id")


class DatasetVersionBase(BaseModel):
    id: int
    version: int
    status: int
    parquet_index_path: Optional[str] = Field(None, alias="parquet_index_path")
    data_count: int = Field(alias="data_count")


class DatasetDetail(BaseModel):
    id: int
    name: str
    description: str
    cover_img: Optional[str] = Field(None, alias="cover_img")
    created_at: int = Field(alias="created_at")
    updated_at: int = Field(alias="update_at")
    user_id: int = Field(alias="user_id")
    username: str
    tags: List[int]
    access_user_ids: Optional[List[int]] = Field(None, alias="access_user_ids")
    is_private: Optional[bool] = Field(None, alias="is_private")
    versions: List[DatasetVersionBase]


class ExtInfo(BaseModel):
    rec_file_path: Optional[str] = Field(None, alias="rec_file_path")
    idx_file_path: Optional[str] = Field(None, alias="idx_file_path")
    json_file_path: Optional[str] = Field(None, alias="json_file_path")
    image_dir_path: Optional[str] = Field(None, alias="image_dir_path")


class CreateDatasetVersionRequest(BaseModel):
    upload_path: str = Field(alias="upload_path")
    description: Optional[str] = None
    dataset_id: int = Field(alias="dataset_id")
    object_cnt: Optional[int] = Field(None, alias="object_cnt")
    data_size: Optional[int] = Field(None, alias="data_size")
    create_by: Optional[int] = Field(None, alias="create_by")
    upload_type: Optional[int] = Field(4, alias="upload_type")
    ext_info: Optional[ExtInfo] = Field(None, alias="ext_info")


class CreateDatasetVersionResponse(BaseModel):
    id: int = Field(alias="id")


class UploadDatasetVersionRequest(BaseModel):
    upload_path: str = Field(alias="upload_path")
    upload_type: int = Field(alias="upload_type")
    dataset_id: int = Field(alias="dataset_id")
    parent_version_id: Optional[int] = Field(None, alias="parent_version_id")
    description: Optional[str] = Field(None, alias="description")


class UploadDatasetVersionResponse(BaseModel):
    id: int = Field(alias="id")


class DatasetVersionDetail(BaseModel):
    id: int
    version: int
    dataset_id: int = Field(alias="dataset_id")
    upload_path: str = Field(alias="upload_path")
    upload_type: int = Field(alias="upload_type")
    parent_version_id: Optional[int] = Field(None, alias="parent_version_id")
    description: Optional[str] = None
    status: int
    message: Optional[str] = None
    created_at: int = Field(alias="created_at")
    user_id: int = Field(alias="user_id")
    data_size: Optional[int] = Field(None, alias="data_size")
    data_count: Optional[int] = Field(None, alias="data_count")
    parquet_index_path: Optional[str] = Field(None, alias="parquet_index_path")
    ext_info: Optional[ExtInfo] = Field(None, alias="ext_info")


class FileUploadData(BaseModel):
    path: str
    url: str
