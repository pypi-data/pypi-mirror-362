# SPDX-FileCopyrightText: 2025 René de Hesselle <dehesselle@web.de>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from enum import Enum
from pathlib import Path
from typing import List, Dict
import subprocess
import shlex
import re
import logging

from .path import path_relative_to

log = logging.getLogger("linkedobj")


class LinkedObject:
    class SystemLinkPath(Enum):
        SYSTEM = "/System"
        USR = "/usr"

    class RelativeLinkPath(Enum):
        EXECUTABLE_PATH = "@executable_path"
        LOADER_PATH = "@loader_path"
        RPATH = "@rpath"

    resolved_rpaths: Dict[Path, None] = dict()  # "ordered set" replacement

    @classmethod
    def is_framework(cls, path: Path) -> bool:
        return ".framework/" in path.as_posix()

    @classmethod
    def is_relative_path(cls, path: Path, relative_to=str()) -> bool:
        if relative_to:
            return path.is_relative_to(relative_to)
        else:
            return (
                path.parts[0] in [item.value for item in LinkedObject.RelativeLinkPath]
                or not path.parent.is_absolute()
            )

    @classmethod
    def is_system_path(cls, path: Path) -> bool:
        # Why 0:2? the leading slash counts as part
        return "".join(path.parts[0:2]) in [item.value for item in cls.SystemLinkPath]

    def __init__(self, path: Path):
        self.path = path
        # TODO: This depends on being populated before we encounter the first lib
        # that uses rpath.
        if not LinkedObject.is_relative_path(self.path):
            self._populate_resolved_rpaths()

    def _make_absolute(self, path: Path) -> Path:
        if LinkedObject.is_relative_path(path) and not LinkedObject.is_framework(path):
            if LinkedObject.is_relative_path(
                path, LinkedObject.RelativeLinkPath.RPATH.value
            ):
                for rpath in self.resolved_rpaths.keys():
                    potential_path = rpath / "/".join(path.parts[1:])
                    if potential_path.is_file():
                        return potential_path
                log.error(f"failed to resolve rpath for {path}")
                return path
            else:
                match self.path.parent.name:
                    case "bin":
                        return self.path.parent.parent / "lib" / path.name
                    case _:
                        return self.path.parent / path.name
        else:
            return path

    def _otool(self, args: str) -> List[str]:
        """Run ``otool`` and return its output.

        Parameters
        ----------
        args : str
            The arguments for the ``otool`` command. This includes options
            and filename.

        Returns
        -------
        List[str]
            The commmand's stdout as list of strings.
        """
        try:
            sp = subprocess.run(
                shlex.split(f"/usr/bin/otool {args} {self.path}"),
                capture_output=True,
                encoding="utf-8",
            )
            sp.check_returncode()
            return sp.stdout.splitlines()
        except subprocess.CalledProcessError:
            log.error(f"otool {args} failed for {self.path}")
            return list()

    def _install_name_tool(self, args: str) -> list:
        try:
            sp = subprocess.run(
                shlex.split(f"/usr/bin/install_name_tool {args} {self.path}"),
                capture_output=True,
                encoding="utf-8",
            )
            sp.check_returncode()
            return sp.stdout.splitlines()
        except subprocess.CalledProcessError:
            log.error(f"install_name_tool {args} failed for {self.path}")
            return list()

    @property
    def install_name(self) -> str:
        result = self._otool("-D")
        return result[1] if len(result) == 2 else ""

    @install_name.setter
    def install_name(self, install_name: str):
        self._install_name_tool(f"-id {install_name}")

    @property
    def rpaths(self) -> List[Path]:
        result = list()
        line_iter = iter(self._otool("-l"))
        for line in line_iter:
            if re.match("\s+cmd LC_RPATH", line):
                next(line_iter)
                if match := re.match("\s+path (.+) \(offset.+", next(line_iter)):
                    result.append(Path(match.group(1)))
        return result

    def _populate_resolved_rpaths(self) -> None:
        for rpath in self.rpaths:
            if rpath.parts[0] in (
                LinkedObject.RelativeLinkPath.LOADER_PATH.value,
                LinkedObject.RelativeLinkPath.EXECUTABLE_PATH.value,
            ):
                LinkedObject.resolved_rpaths[
                    (self.path.parent / "/".join(rpath.parts[1:])).resolve()
                ] = None

    def add_rpath(self, rpath: str):
        self._install_name_tool(f"-add_rpath {rpath}")

    def change_one_dependant_install_name(self, install_name: str):
        if libs := [l for l in self.depends_on() if Path(install_name).name in l]:
            self._install_name_tool(f"-change {libs[0]} {install_name}")

    def change_dependent_install_names(self, install_name: Path, lib_dir: Path):
        # Create a list of of all libraries in lib_dir and in the first level
        # of subdirectories (excluding frameworks).
        libraries = list()
        libraries.extend(lib_dir.glob("*.[dylib so]*"))
        for path in lib_dir.iterdir():
            if path.is_dir() and path.suffix != ".framework":
                libraries.extend(path.glob("*.[dylib so]*"))

        # Match the libraries that self depends on to that list above and
        # change install name accordingly.
        for dependent_library in self.depends_on():
            if matched_library := next(
                (_ for _ in libraries if dependent_library.name in _.name), None
            ):
                self._install_name_tool(
                    "-change {} {}".format(
                        dependent_library,
                        install_name / path_relative_to(matched_library, "Frameworks"),
                    )
                )

    def clear_rpath(self):
        for rpath in self.rpath:
            self._install_name_tool(f"-delete_rpath {rpath}")

    def depends_on(self, exclude_system: bool = False) -> List[Path]:
        result = list()

        if LinkedObject.is_framework(self.path):
            log.debug(f"intentionally skipping framework library {self.path}")
        else:
            skip_lines = 2 if self.install_name else 1
            for line in self._otool("-L")[skip_lines:]:
                # This matches only dylibs:
                # match = re.match("\t(.+\.dylib)", line)
                # This will match everything:
                if match := re.match("\t(.+) \(compatibility", line):
                    library = Path(match.group(1))
                    if exclude_system:
                        if not LinkedObject.is_system_path(library):
                            result.append(library)
                    else:
                        result.append(library)
        return result

    def flattened_dependency_tree(
        self, exclude_system: bool = False, _dependencies=list()
    ) -> List[Path]:
        for library in self.depends_on(exclude_system):
            library = self._make_absolute(library)
            if library not in _dependencies:
                _dependencies.append(library)
                for l in LinkedObject(library).flattened_dependency_tree(
                    exclude_system,
                    _dependencies,
                ):
                    if l not in _dependencies:
                        _dependencies.append(l)
        return _dependencies
