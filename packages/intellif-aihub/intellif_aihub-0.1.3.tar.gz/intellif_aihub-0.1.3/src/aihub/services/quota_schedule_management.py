from __future__ import annotations

import os
from pathlib import Path

_ENV_KEY = "PRE_STOP_SENTINEL_FILE"
_DEFAULT_SENTINEL = "/tmp/pre_stop_sentinel_file"
_SENTINEL_PATH = Path(os.getenv(_ENV_KEY, _DEFAULT_SENTINEL))


def is_pre_stopped() -> bool:
    return _SENTINEL_PATH.exists()


class PreStopService:
    @staticmethod
    def is_pre_stopped() -> bool:
        return is_pre_stopped()
