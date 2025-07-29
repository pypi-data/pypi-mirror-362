from __future__ import annotations

import unittest

from src.aihub.client import Client

BASE_URL = "http://192.168.13.160:30021"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTIwNDgzOTgsImlhdCI6MTc1MTQ0MzU5OCwidWlkIjoxMH0.GqFDpRQuRlNx9YdHlC6zql-8_ZtCpDV4zUFvqM5p7EE"


class TestDatasetManagement(unittest.TestCase):
    def test_create_dataset_and_version(self):
        client = Client(base_url=BASE_URL, token=TOKEN)
        dataset_id, dataset_version_id, version_tag = client.dataset_management.create_dataset_and_version(
            dataset_name="sdk-dataset",
            dataset_description="xxxxx",
            is_local_upload=True,
            local_file_path=r"C:\Users\admin\PycharmProjects\aitcsdk\images.zip",
            server_file_path="",
            version_description="yyyyy",
        )
        print("dataset_id:", dataset_id)
        print("dataset_version_id:", dataset_version_id)
        print("version_tag:", version_tag)

    def test_run_download(self):
        client = Client(base_url=BASE_URL, token=TOKEN)
        client.dataset_management.run_download(dataset_version_name="re/V12",
                                               local_dir=r"C:\Users\admin\Downloads\ljn", worker=4)
        print("Done!")
