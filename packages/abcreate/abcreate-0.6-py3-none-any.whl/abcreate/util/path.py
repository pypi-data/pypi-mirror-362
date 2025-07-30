# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
from pathlib import Path

log = logging.getLogger("path")


def path_relative_to(path: Path, part: str, include_part: bool = False) -> Path:
    try:
        index = path.parts.index(part)
        offset = 0 if include_part else 1
        return Path(*path.parts[index + offset :])
    except ValueError:
        log.error(ValueError)
        return path
