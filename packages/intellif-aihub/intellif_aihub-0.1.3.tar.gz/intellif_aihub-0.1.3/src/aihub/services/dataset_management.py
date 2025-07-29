from __future__ import annotations

import mimetypes
import os
import pathlib

import httpx

from ..exceptions import APIError
from ..models.common import APIWrapper
from ..models.dataset_management import *
from ..utils.download import dataset_download

_BASE = "/dataset-mng/api/v2"


class DatasetManagementService:
    """数据集管理服务，用于数据集的上传、下载

    Methods:
        create_dataset_and_version: 创建数据集版本
        run_download: 下载


    """

    def __init__(self, http: httpx.Client):
        self._dataset = _Dataset(http)
        self._dataset_version = _DatasetVersion(http)
        self._upload = _Upload(http)

    # 直接把常用方法抛到一级，调用体验简单
    def create_dataset(self, payload: CreateDatasetRequest) -> int:
        return self._dataset.create(payload)

    def get_dataset(self, dataset_id: int) -> DatasetDetail:
        return self._dataset.get(dataset_id)

    def create_dataset_version(self, payload: CreateDatasetVersionRequest) -> int:
        return self._dataset_version.create(payload)

    def upload_dataset_version(self, payload: UploadDatasetVersionRequest) -> int:
        return self._dataset_version.upload(payload)

    def get_dataset_version(self, version_id: int) -> DatasetVersionDetail:
        return self._dataset_version.get(version_id)

    def get_dataset_version_by_name(self, version_name: str) -> DatasetVersionDetail:
        return self._dataset_version.get_by_name(version_name)

    def upload_file(self, file_path: str) -> FileUploadData:
        return self._upload.upload_file(file_path)

    # 如果想要访问子对象，也保留属性
    @property
    def dataset(self) -> _Dataset:
        return self._dataset

    @property
    def dataset_version(self) -> _DatasetVersion:
        return self._dataset_version

    def create_dataset_and_version(
        self,
        *,
        dataset_name: str,
        dataset_description: str = "",
        is_local_upload: bool,
        local_file_path: str | None = None,
        server_file_path: str | None = None,
        version_description: str = "",
    ) -> tuple[int, int, str]:
        """创建数据集及其版本。

        根据参数创建数据集，并根据上传类型（本地或服务器路径）创建对应的数据集版本。

        Args:
            dataset_name: 数据集名称。
            dataset_description: 数据集描述，默认为空。
            is_local_upload: 是否为本地上传。若为 True，需提供 local_file_path；
                             否则需提供 server_file_path。
            local_file_path: 本地文件路径，当 is_local_upload=True 时必须提供。
            server_file_path: 服务器已有文件路径，当 is_local_upload=False 时必须提供。
            version_description: 版本描述，默认为空。

        Returns:
           tuple[int, int, str]: 一个三元组，包含：[数据集 ID,数据集版本 ID, 数据集版本标签（格式为 <dataset_name>/V<version_number>)]
        """
        if is_local_upload:
            if not local_file_path:
                raise ValueError("is_local_upload=True 时必须提供 local_file_path")
            upload_type = 1
        else:
            if not server_file_path:
                raise ValueError("is_local_upload=False 时必须提供 server_file_path")
            upload_type = 3

        dataset_id = self._dataset.create(
            CreateDatasetRequest(
                name=dataset_name,
                description=dataset_description,
                tags=[],
            )
        )

        if is_local_upload:
            upload_data = self._upload.upload_file(local_file_path)
            upload_path = upload_data.path
        else:
            upload_path = server_file_path

        version_id = self._dataset_version.upload(
            UploadDatasetVersionRequest(
                upload_path=upload_path,
                upload_type=upload_type,
                dataset_id=dataset_id,
                description=version_description,
            )
        )

        detail = self._dataset.get(dataset_id)
        ver_num = next(
            (v.version for v in detail.versions if v.id == version_id),
            None,
        )
        if ver_num is None:
            ver_num = 1

        version_tag = f"{detail.name}/V{ver_num}"

        return dataset_id, version_id, version_tag

    def run_download(
        self, dataset_version_name: str, local_dir: str, worker: int = 4
    ) -> None:
        """根据数据集版本名称下载对应的数据集文件。

        Args:
            dataset_version_name (str): 数据集版本名称。
            local_dir (str): 下载文件保存的本地目录路径。
            worker (int): 并发下载使用的线程数，默认为 4。

        Raises:
            APIError: 如果获取到的版本信息中没有 parquet_index_path，即无法进行下载时抛出异常。

        Returns:
            None
        """
        detail = self._dataset_version.get_by_name(dataset_version_name)
        if not detail.parquet_index_path:
            raise APIError("parquet_index_path 为空")
        dataset_download(detail.parquet_index_path, local_dir, worker)


class _Dataset:
    def __init__(self, http: httpx.Client):
        self._http = http

    def create(self, payload: CreateDatasetRequest) -> int:
        resp = self._http.post(
            f"{_BASE}/datasets",
            json=payload.model_dump(by_alias=True, exclude_none=True),
        )
        wrapper = APIWrapper[CreateDatasetResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data.id

    def get(self, dataset_id: int) -> DatasetDetail:
        resp = self._http.get(f"{_BASE}/datasets/{dataset_id}")
        wrapper = APIWrapper[DatasetDetail].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data


class _DatasetVersion:
    def __init__(self, http: httpx.Client):
        self._http = http

    def create(self, payload: CreateDatasetVersionRequest) -> int:
        resp = self._http.post(
            f"{_BASE}/dataset-versions",
            json=payload.model_dump(by_alias=True, exclude_none=True),
        )
        wrapper = APIWrapper[CreateDatasetVersionResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data.id

    def upload(self, payload: UploadDatasetVersionRequest) -> int:
        resp = self._http.post(
            f"{_BASE}/dataset-versions-upload",
            json=payload.model_dump(by_alias=True, exclude_none=True),
        )
        wrapper = APIWrapper[UploadDatasetVersionResponse].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data.id

    def get(self, version_id: int) -> DatasetVersionDetail:
        resp = self._http.get(f"{_BASE}/dataset-versions/{version_id}")
        wrapper = APIWrapper[DatasetVersionDetail].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data

    def get_by_name(self, version_name: str) -> DatasetVersionDetail:
        resp = self._http.get(
            f"{_BASE}/dataset-versions-detail", params={"name": version_name}
        )
        wrapper = APIWrapper[DatasetVersionDetail].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data


class _Upload:
    def __init__(self, http: httpx.Client):
        self._http = http

    def upload_file(self, file_path: str) -> FileUploadData:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(file_path)

        file_name = pathlib.Path(file_path).name
        mime_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"

        with open(file_path, "rb") as fp:
            resp = self._http.post(
                f"/dataset-mng/api/v1/uploads",
                files={"file": (file_name, fp, mime_type)},
                timeout=None,
            )

        wrapper = APIWrapper[FileUploadData].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")

        return wrapper.data
