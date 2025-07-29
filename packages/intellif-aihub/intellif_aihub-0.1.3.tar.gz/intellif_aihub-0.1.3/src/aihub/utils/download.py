from __future__ import annotations

import concurrent.futures
import os
import tempfile
from typing import List, TypedDict

import pyarrow.parquet as pq
from tqdm import tqdm

from .http import http_download_file
from .s3 import s3_to_url


class DatasetParquetMeta(TypedDict):
    parent_dir: str
    name: str
    s3path: str
    type: int  # 0=file, 1=dir


_ENUM_FILE = 0


def _read_parquet_index(file_path: str) -> List[DatasetParquetMeta]:
    table = pq.read_table(file_path)
    return table.to_pylist()  # 每行转 dict


def _safe_rel(part: str) -> str:
    if not part:
        return ""
    drive, tail = os.path.splitdrive(part)
    return tail.lstrip(r"\/")


def dataset_download(index_url: str, local_dir: str, worker: int = 4) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_file = os.path.join(tmpdir, "index.parquet")
        http_download_file(index_url, tmp_file)
        rows = _read_parquet_index(tmp_file)

    host = (index_url.split("//", 1)[-1]).split("/", 1)[0]

    files = [
        (
            os.path.join(
                local_dir,
                _safe_rel(row["parent_dir"]),
                _safe_rel(row["name"]),
            ),
            s3_to_url(row["s3path"], host),
        )
        for row in rows if row["type"] == _ENUM_FILE
    ]

    if worker < 1:
        worker = 1

    with tqdm(total=len(files), desc="Downloading dataset") as bar, \
            concurrent.futures.ThreadPoolExecutor(max_workers=worker) as pool:

        def _one(flocal: str, furl: str):
            http_download_file(furl, flocal)
            bar.update()

        futures = [pool.submit(_one, p, u) for p, u in files]
        for fut in concurrent.futures.as_completed(futures):
            fut.result()
