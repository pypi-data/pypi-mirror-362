# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
from pathlib import Path
from shutil import copy

from pydantic_xml import BaseXmlModel

from abcreate.util import path_relative_to

log = logging.getLogger("locale")


class Locale(BaseXmlModel):
    name: str

    def install(self, bundle_dir: Path, install_prefix: Path):
        target_dir = bundle_dir / "Contents" / "Resources" / "share" / "locale"

        for source_path in Path(install_prefix / "share" / "locale").rglob(self.name):
            target_path = target_dir / path_relative_to(source_path, "locale")
            if target_path.exists():
                pass
                # log.debug(f"will not overwrite {target_path}")
            else:
                log.debug(f"copy {source_path} to {target_path}")
                target_path.parent.mkdir(parents=True, exist_ok=True)
                copy(source_path, target_path)
