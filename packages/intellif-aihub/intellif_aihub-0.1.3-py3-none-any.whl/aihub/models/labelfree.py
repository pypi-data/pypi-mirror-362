from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Stats(BaseModel):
    """标注统计信息"""

    total_annotations: int = Field(alias="total_annotations")
    labeled_annotations: int = Field(alias="labeled_annotations")
    total_labels: int = Field(alias="total_labels")
    total_reviews: Optional[int] = Field(None, alias="total_reviews")
    unlabeled_reviews: Optional[int] = Field(None, alias="unlabeled_reviews")
    labeled_reviews: Optional[int] = Field(None, alias="labeled_reviews")
    accepted_count: Optional[int] = Field(None, alias="accepted_count")
    rejected_count: Optional[int] = Field(None, alias="rejected_count")


class GetGlobalStatsResponse(BaseModel):
    """
    标注统计概况
    """

    global_stats: Stats = Field(alias="global_stats")
    valid_ten_percent: bool = Field(alias="valid_ten_percent")
    valid_fifty_percent: bool = Field(alias="valid_fifty_percent")
    valid_hundred_percent: bool = Field(alias="valid_hundred_percent")
    data_exported_count: int = Field(alias="data_exported_count")
    exported_dataset_name: str = Field(alias="exported_dataset_name")
