# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
import os
from pathlib import Path

from pydantic_xml import BaseXmlModel

log = logging.getLogger("symlink")


class Symlink(BaseXmlModel):
    source_path: Path

    def install(self, bundle_dir: Path):
        target_dir = bundle_dir / "Contents" / "MacOS"

        target_path = target_dir / self.source_path.name

        if target_path.exists():
            log.debug(f"will not overwrite {target_path}")
        else:
            log.debug(f"symlinking {self.source_path} to {target_path}")
            target_path.parent.mkdir(parents=True, exist_ok=True)
            os.symlink(src=self.source_path, dst=target_path)
