# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
from pathlib import Path
from typing import List

from pydantic_xml import BaseXmlModel, element

from .library import Library

log = logging.getLogger("library")


class Libraries(BaseXmlModel):
    libraries: List[Library] = element(tag="library")

    def install(self, bundle_dir: Path, install_prefix: Path):
        for library in self.libraries:
            library.install(bundle_dir, install_prefix)
