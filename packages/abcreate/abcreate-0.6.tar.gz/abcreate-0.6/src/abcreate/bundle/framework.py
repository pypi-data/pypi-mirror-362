# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
from pathlib import Path
from shutil import copytree

from pydantic_xml import BaseXmlModel

log = logging.getLogger("framework")


class Framework(BaseXmlModel):
    source_path: Path

    def install(self, bundle_dir: Path, install_prefix: Path):
        target_dir = bundle_dir / "Contents" / "Frameworks"

        if not target_dir.exists():
            log.debug(f"creating {target_dir}")
            target_dir.mkdir(parents=True)

        if (source_path := install_prefix / self.source_path).exists():
            target_path = target_dir / self.source_path.name
            if target_path.exists():
                log.error(f"will not overwrite {target_path}")
            else:
                log.debug(f"copy {source_path} to {target_path}")
                copytree(source_path, target_path, symlinks=True)
        else:
            log.error(f"cannot locate {self.source_path}")
