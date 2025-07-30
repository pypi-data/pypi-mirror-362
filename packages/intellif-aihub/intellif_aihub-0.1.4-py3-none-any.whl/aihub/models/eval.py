# !/usr/bin/env python
# -*-coding:utf-8 -*-
from pydantic import BaseModel


class CreatEvalReq(BaseModel):
    dataset_id: int
    dataset_version_id: int
    prediction_artifact_path: str
    evaled_artifact_path: str
    run_id: str
    user_id: int = 0
    report: dict = {}


class CreatEvalResp(BaseModel):
    id: int
