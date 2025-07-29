# Copyright 2025 Hanzo Industries Inc.
# SPDX-License-Identifier: Apache-2.0

from typing import Protocol


class SandboxCodeToolbox(Protocol):
    def get_default_image(self) -> str:
        ...

    def get_code_run_command(self, code: str) -> str:
        ...

    def get_code_run_args(self) -> list[str]:
        ...

    # ... other protocol methods
