# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
from pathlib import Path
from typing import Optional
from shutil import copy

from pydantic_xml import BaseXmlModel, attr

from abcreate.util import LinkedObject
from .library import Library

log = logging.getLogger("executable")


class Executable(BaseXmlModel):
    name: Optional[Path] = attr(default=None)
    source_path: Path

    @property
    def target_name(self) -> str:
        return (self.name or self.source_path).name

    def install(self, bundle_dir: Path, install_prefix: Path):
        target_dir = bundle_dir / "Contents" / "MacOS"
        if not target_dir.exists():
            target_dir.mkdir(parents=True)

        if (source_path := install_prefix / "bin" / self.source_path).exists():
            target_path = target_dir / self.target_name
            if target_path.exists():
                log.error(f"will not overwrite {target_path}")
            else:
                log.debug(f"copy {source_path} to {target_path}")
                copy(source_path, target_path)

                # pull in dependencies
                linked_object = LinkedObject(source_path)
                if not linked_object.rpaths:
                    log.debug(f"assuming lib as default rpath for {source_path}")
                    linked_object.resolved_rpaths[install_prefix / "lib"] = None
                for path in linked_object.flattened_dependency_tree(
                    exclude_system=True
                ):
                    library = Library(source_path=path)
                    if library.is_framework:
                        # frameworks are taken care of separately
                        log.debug(
                            f"intentionally skipping framework library {library.source_path}"
                        )
                        pass
                    else:
                        library.install(bundle_dir, install_prefix)

                # adjust install names
                frameworks_dir = bundle_dir / "Contents" / "Frameworks"
                linked_object = LinkedObject(target_path)
                linked_object.change_dependent_install_names(
                    Path("@executable_path/../Frameworks"),
                    frameworks_dir,
                )
        else:
            log.error(f"cannot locate {self.source_path}")
