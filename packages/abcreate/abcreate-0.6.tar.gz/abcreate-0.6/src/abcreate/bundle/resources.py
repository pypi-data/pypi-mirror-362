# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
from pathlib import Path
from typing import List

from pydantic_xml import BaseXmlModel, element

from .resource import Resource

log = logging.getLogger("resource")


class Resources(BaseXmlModel):
    resources: List[Resource] = element(tag="resource")

    def install(self, bundle_dir: Path, install_prefix: Path):
        for resource in self.resources:
            resource.install(bundle_dir, install_prefix)
