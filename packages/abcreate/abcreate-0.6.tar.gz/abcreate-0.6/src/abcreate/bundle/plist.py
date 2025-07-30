# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from pathlib import Path
import logging
from importlib.resources import files
from shutil import copy
from enum import Enum
from typing import Optional, ClassVar
import plistlib

from pydantic_xml import BaseXmlModel

log = logging.getLogger("plist")

INFO_PLIST = files("abcreate.bundle") / "Info.plist"


class Plist(BaseXmlModel):
    source_path: Optional[Path] = None
    target_path: ClassVar[Path] = None

    class Key(Enum):
        CFBUNDLEEXECUTABLE = "CFBundleExecutable"
        CFBUNDLEICONFILE = "CFBundleIconFile"
        CFBUNDLELOCALIZATIONS = "CFBundleLocalizations"

    def install(self, bundle_dir: Path, install_prefix: Path):
        target_dir = bundle_dir / "Contents"
        Plist.target_path = target_dir / "Info.plist"
        if Plist.target_path.exists():
            log.debug(f"already installed {Plist.target_path}")
        else:
            target_dir.mkdir(parents=True, exist_ok=True)
            if self.source_path:
                source_path = install_prefix / self.source_path
            else:
                source_path = INFO_PLIST

            log.debug(f"copy {source_path} to {Plist.target_path}")
            copy(source_path, Plist.target_path)

    def _write(self, key: str, value: str):
        if plist := self._read_all():
            plist[key] = value
            with open(Plist.target_path, "wb") as file:
                plistlib.dump(plist, file)

    def _read_all(self):
        if Plist.target_path and Plist.target_path.exists():
            with open(Plist.target_path, "rb") as file:
                return plistlib.load(file)
        else:
            log.error("Info.plist hasn't been installed yet")
            return None

    def _read(self, key: str) -> str:
        if plist := self._read_all():
            return plist[key]
        else:
            return str()

    @property
    def CFBundleExecutable(self) -> str:
        return self._read(self.Key.CFBUNDLEEXECUTABLE.value)

    @CFBundleExecutable.setter
    def CFBundleExecutable(self, value):
        self._write(self.Key.CFBUNDLEEXECUTABLE.value, value)

    @property
    def CFBundleIconFile(self) -> str:
        return self._read(self.Key.CFBUNDLEICONFILE.value)

    @CFBundleIconFile.setter
    def CFBundleIconFile(self, value):
        self._write(self.Key.CFBUNDLEICONFILE.value, value)

    @property
    def CFBundleLocalizations(self):
        return self._read(self.Key.CFBUNDLELOCALIZATIONS.value)

    @CFBundleLocalizations.setter
    def CFBundleLocalizations(self, value):
        self._write(self.Key.CFBUNDLELOCALIZATIONS.value, value)
