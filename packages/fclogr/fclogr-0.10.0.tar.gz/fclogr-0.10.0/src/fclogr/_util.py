# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

import re

PERCENT_MATCHER = re.compile("%([^%])?")


def escape_percentage(value: str) -> str:
    return PERCENT_MATCHER.sub(r"%%\1", value)
