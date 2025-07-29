from __future__ import annotations

import unittest

from src.aihub.client import Client

BASE_URL = "http://192.168.13.160:30021"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTIwNDgzOTgsImlhdCI6MTc1MTQ0MzU5OCwidWlkIjoxMH0.GqFDpRQuRlNx9YdHlC6zql-8_ZtCpDV4zUFvqM5p7EE"


class TestLabelfree(unittest.TestCase):
    def test_get_global_stats(self):
        client = Client(base_url=BASE_URL, token=TOKEN)
        resp = client.labelfree.get_project_global_stats(project_name="project_178021")
        print("resp:", resp)
