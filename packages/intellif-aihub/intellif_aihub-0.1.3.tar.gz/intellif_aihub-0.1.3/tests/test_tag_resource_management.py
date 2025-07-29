from __future__ import annotations

import unittest

from src.aihub.client import Client
from src.aihub.models.tag_resource_management import *

BASE_URL = "http://192.168.13.160:30021"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTI4MDg2NDgsImlhdCI6MTc1MjIwMzg0OCwidWlkIjoxMH0.Ha1Qt2KbUtbvcvtLTBvrMLrtnKsKHZ2eIuYpvI01sus"


class TestTagResourceManagement(unittest.TestCase):
    def test_virtual_cluster(self) -> None:
        client = Client(base_url=BASE_URL, token=TOKEN)
        svcs = client.tag_resource_management.select_virtual_clusters(
            SelectVirtualClustersRequest(user_id=10, module_type=4)
        )
        self.assertIsInstance(svcs, list)
