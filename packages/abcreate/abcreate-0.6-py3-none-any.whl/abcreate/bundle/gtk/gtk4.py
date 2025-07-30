# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
from pathlib import Path

from pydantic_xml import BaseXmlModel

from abcreate.bundle.library import Library
from abcreate.bundle.locale import Locale
from abcreate.bundle.resource import Resource
from .gdkpixbuf import GdkPixbuf
from .glib import Glib

log = logging.getLogger("gtk")


class Gtk4(BaseXmlModel):
    def _install_frameworks(self, bundle_dir: Path, source_dir: Path):
        library = Library(source_path=Path("libgtk-4.1.dylib"))
        library.install(bundle_dir, source_dir)

        for source_path in Path(
            source_dir / "lib" / "gtk-4.0" / "4.0.0" / "printbackends"
        ).glob("*.so"):
            library = Library(source_path=source_path)
            # Why flatten? We need to get rid of the subdirectories as e.g.
            # "4.0.0" in a path does not pass validation when signing.
            library.install(bundle_dir, source_dir, flatten=True)

    def _install_resources(self, bundle_dir: Path, source_dir: Path):
        resource = Resource(source_path=Path("share/gtk-4.0"))
        resource.install(bundle_dir, source_dir)

        locale = Locale(name="gtk40.mo")
        locale.install(bundle_dir, source_dir)

    def install(self, bundle_dir: Path, source_dir: Path):
        glib = Glib()
        glib.install(bundle_dir, source_dir)
        gdkpixbuf = GdkPixbuf()
        gdkpixbuf.install(bundle_dir, source_dir)
        self._install_frameworks(bundle_dir, source_dir)
        self._install_resources(bundle_dir, source_dir)
