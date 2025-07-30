# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
from pathlib import Path
from typing import List

from pydantic_xml import BaseXmlModel, element

from .locale import Locale
from .plist import Plist

log = logging.getLogger("locale")


class Locales(BaseXmlModel):
    locales: List[Locale] = element(tag="locale")

    @property
    def main_locale(self) -> Locale:
        try:
            return self.locales[0]
        except IndexError:
            log.error("no locales specified")
            return None

    def install(self, bundle_dir: Path, install_prefix: Path):
        for locale in self.locales:
            locale.install(bundle_dir, install_prefix)

        if locale := self.main_locale:
            Plist().CFBundleLocalizations = [
                path.parent.parent.name
                for path in (
                    bundle_dir / "Contents" / "Resources" / "share" / "locale"
                ).rglob(locale.name)
            ]
