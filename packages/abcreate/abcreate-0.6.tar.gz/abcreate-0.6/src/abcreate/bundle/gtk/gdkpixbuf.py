# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
from pathlib import Path
import re

from pydantic_xml import BaseXmlModel

from abcreate.bundle.library import Library

log = logging.getLogger("gdkpixbuf")


class GdkPixbuf(BaseXmlModel):
    def install(self, bundle_dir: Path, source_dir: Path):
        # pixbuf loaders: *.so files
        target_dir = bundle_dir / "Contents" / "Frameworks"
        for source_path in Path(
            source_dir / "lib" / "gdk-pixbuf-2.0" / "2.10.0" / "loaders"
        ).glob("*.so"):
            library = Library(source_path=source_path)
            # Why flatten? We need to get rid of the subdirectories as e.g.
            # "2.10.0" in a path does not pass validation when signing.
            library.install(bundle_dir, source_dir, flatten=True)

        # pixbuf loaders: loaders.cache file
        target_dir = bundle_dir / "Contents" / "Resources"
        source_path = Path(
            source_dir / "lib" / "gdk-pixbuf-2.0" / "2.10.0" / "loaders.cache"
        )
        loaders_cache = source_path.read_text()
        # Since we're breaking up the original structure, best place for
        # loaders.cache is etc as it is a configuration file after all.
        target_path = target_dir / "etc" / "loaders.cache"
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, "wt") as file:
            for line in loaders_cache.splitlines(keepends=True):
                if match := re.match('".+(libpixbufloader.+\.so)"', line):
                    file.write(f'"Frameworks/{match.group(1)}"\n')
                else:
                    file.write(line)
