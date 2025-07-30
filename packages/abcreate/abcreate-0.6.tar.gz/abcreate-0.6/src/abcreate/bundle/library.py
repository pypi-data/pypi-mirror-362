# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
from pathlib import Path
from shutil import copy

from pydantic_xml import BaseXmlModel
from pydantic import field_validator

from abcreate.util import LinkedObject, path_relative_to


log = logging.getLogger("library")


class Library(BaseXmlModel):
    source_path: Path

    @property
    def is_framework(self) -> bool:
        return any(".framework" in part for part in self.source_path.parts)

    def install(self, bundle_dir: Path, install_prefix: Path, flatten: bool = False):
        target_dir = bundle_dir / "Contents" / "Frameworks"
        if not target_dir.exists():
            log.debug(f"creating {target_dir}")
            target_dir.mkdir(parents=True)

        for source_path in (install_prefix / "lib" / self.source_path.parent).glob(
            self.source_path.name
        ):
            if source_path.exists():
                if flatten:
                    target_path = target_dir / source_path.name
                else:
                    target_path = target_dir / path_relative_to(source_path, "lib")
                if target_path.exists():
                    pass
                    # log.debug(f"will not overwrite {target_path}")
                else:
                    if not target_path.parent.exists():
                        # for subdirectories in the libraries directory
                        target_path.parent.mkdir(parents=True)

                    log.debug(f"copy {source_path} to {target_path}")
                    copy(source_path, target_path)

                    # pull in dependencies
                    linked_object = LinkedObject(source_path)
                    for path in linked_object.flattened_dependency_tree(
                        exclude_system=True
                    ):
                        library = Library(source_path=path)
                        if library.is_framework:
                            # frameworks are taken care of separately
                            log.debug(
                                f"intentionally skipping framework library {library.source_path}"
                            )
                        else:
                            library.install(bundle_dir, install_prefix)

                    # adjust install names
                    linked_object = LinkedObject(target_path)
                    loader_path = Path("@loader_path")
                    if not flatten:
                        # take care of nested directory structure
                        for _ in range(
                            len(path_relative_to(source_path, "lib").parts) - 1
                        ):
                            loader_path /= ".."
                    linked_object.change_dependent_install_names(
                        loader_path, target_dir
                    )
            else:
                log.error(f"cannot locate {self.source_path}")
