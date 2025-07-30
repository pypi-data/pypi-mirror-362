# !/usr/bin/env python
# -*-coding:utf-8 -*-
import httpx

from ..exceptions import APIError
from ..models.common import APIWrapper
from ..models.eval import CreatEvalReq, CreatEvalResp

_BASE = "/eval-platform/api/v1"


class EvalService:
    """评测服务"""

    def __init__(self, http: httpx.Client):
        self._http = http
        self._eval = _Eval(http)

    def create(
        self,
        dataset_version_name: str,
        prediction_artifact_path: str,
        evaled_artifact_path: str,
        report_json: dict,
        run_id,
    ) -> int:
        """创建评测报告

        Args:
            run_id (str): RUN ID
            report_json (dict): 报告内容
            evaled_artifact_path:   评测结果制品路径
            prediction_artifact_path: 推理结果制品路径
            dataset_version_name (str): 数据集名称


        Returns:
            id (int): 评测报告id

        """
        from .dataset_management import DatasetManagementService

        dataset_service = DatasetManagementService(self._http)
        dataset_version = dataset_service.get_dataset_version_by_name(
            dataset_version_name
        )
        payload = CreatEvalReq(
            dataset_id=dataset_version.dataset_id,
            dataset_version_id=dataset_version.id,
            evaled_artifact_path=evaled_artifact_path,
            prediction_artifact_path=prediction_artifact_path,
            report=report_json,
            run_id=run_id,
        )

        return self._eval.create(payload)


class _Eval:
    def __init__(self, http: httpx.Client):
        self._http = http

    def create(self, payload: CreatEvalReq) -> int:
        resp = self._http.post(f"{_BASE}/RUN/", json=payload.model_dump())
        wrapper = APIWrapper[CreatEvalResp].model_validate(resp.json())
        if wrapper.code != 0:
            raise APIError(f"backend code {wrapper.code}: {wrapper.msg}")
        return wrapper.data.id
