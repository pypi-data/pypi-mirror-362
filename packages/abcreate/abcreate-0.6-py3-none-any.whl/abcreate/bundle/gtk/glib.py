# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
from pathlib import Path

from pydantic_xml import BaseXmlModel

from abcreate.bundle.library import Library
from abcreate.bundle.resource import Resource

log = logging.getLogger("glib")


class Glib(BaseXmlModel):
    def install(self, bundle_dir: Path, source_dir: Path):
        library = Library(source_path=Path("libglib-2.0.0.dylib"))
        library.install(bundle_dir, source_dir)

        for source_path in Path(source_dir / "lib" / "gio" / "modules").glob("*.so"):
            library = Library(source_path=source_path)
            # We cannot flatten here because GIO_MODULE_DIR expects a dedicated
            # directory (it will try to load everything in there, throwing warning
            # for libraries which are not GIO modules).
            library.install(bundle_dir, source_dir)

        resource = Resource(source_path=Path("share/glib-2.0"))
        resource.install(bundle_dir, source_dir)
