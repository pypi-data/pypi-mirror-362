# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pydantic import BaseModel


class SourceValidator(BaseModel):
    """
    Source code params.
    """

    source: str = None
    "Pointer to source code."

    handler: str = None
    "Function entrypoint."

    code: str = None
    "Source code (plain text)."

    base64: str = None
    "Source code (base64 encoded)."

    lang: str = None
    "Source code language (hint)."
