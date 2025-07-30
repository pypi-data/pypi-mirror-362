# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

import logging
from pathlib import Path
from shutil import rmtree
from typing import Optional

from pydantic import model_validator
from pydantic_xml import BaseXmlModel, element

from .executables import Executables
from .frameworks import Frameworks
from .gtk import Gir, Gtk3, Gtk4
from .icons import Icons
from .libraries import Libraries
from .locales import Locales
from .plist import Plist
from .resources import Resources

log = logging.getLogger("bundle")


class Bundle(BaseXmlModel, tag="bundle"):
    executables: Executables
    frameworks: Optional[Frameworks] = element(default=None)
    gir: Gir
    gtk3: Optional[Gtk3] = element(default=None)
    gtk4: Optional[Gtk4] = element(default=None)
    icons: Icons
    libraries: Optional[Libraries] = element(default=None)
    locales: Locales
    plist: Plist
    resources: Resources

    @model_validator(mode="after")
    def ensure_gtk3_gtk4_mutually_exclusive(self):
        if (self.gtk3 and self.gtk4) or (not self.gtk3 and not self.gtk4):
            log.critical("gtk3 and gtk4 are mutually exclusive")
        return self

    def create(self, output_dir: Path, install_prefix: Path):
        bundle_dir = output_dir / Path(
            self.executables.main_executable.target_name
        ).with_suffix(".app")

        if bundle_dir.exists():
            log.debug(f"removing {bundle_dir.as_posix()}")
            rmtree(bundle_dir)

        log.info(f"creating {bundle_dir.as_posix()}")
        bundle_dir.mkdir(parents=True)

        # It's important to install the plist first because others might
        # depend on it. (There is no dependency management.)
        log.info("--- {:>11} ---".format("plist"))
        self.plist.install(bundle_dir, install_prefix)
        if self.gtk3:
            log.info("--- {:>11} ---".format("gtk3"))
            self.gtk3.install(bundle_dir, install_prefix)
        if self.gtk4:
            log.info("--- {:>11} ---".format("gtk4"))
            self.gtk4.install(bundle_dir, install_prefix)
        log.info("--- {:>11} ---".format("gir"))
        self.gir.install(bundle_dir, install_prefix)
        if self.libraries:
            log.info("--- {:>11} ---".format("libraries"))
            self.libraries.install(bundle_dir, install_prefix)
        if self.frameworks:
            log.info("--- {:>11} ---".format("frameworks"))
            self.frameworks.install(bundle_dir, install_prefix)
        log.info("--- {:>11} ---".format("executables"))
        self.executables.install(bundle_dir, install_prefix)
        log.info("--- {:>11} ---".format("icons"))
        self.icons.install(bundle_dir, install_prefix)
        log.info("--- {:>11} ---".format("locales"))
        self.locales.install(bundle_dir, install_prefix)
        log.info("--- {:>11} ---".format("resources"))
        self.resources.install(bundle_dir, install_prefix)
