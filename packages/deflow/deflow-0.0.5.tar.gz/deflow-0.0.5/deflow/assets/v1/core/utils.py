# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from ddeutil.io import YamlEnvFl, is_ignored, read_ignore

from ....__types import DictData
from .__types import Re


def get_stream(name: str, path: Path) -> DictData:
    """Get Stream data that store on an input config path.

    :param name: A stream name that want to search and extract data from the
        config path.
    :param path: A config path.

    :rtype: DictData
    """
    d: Path
    ignore = read_ignore(path / ".confignore")
    for d in path.rglob("*"):
        if d.is_dir() and d.stem == name:
            cfile: Path = d / "config.yml"

            if is_ignored(cfile, ignore):
                continue

            if not cfile.exists():
                raise FileNotFoundError(
                    f"Get stream file: {cfile.name} does not exist."
                )

            data: DictData = YamlEnvFl(path=cfile).read()
            if name not in data:
                raise ValueError(
                    f"Stream config does not set {name!r} config data."
                )
            elif "type" not in (stream_data := data[name]):
                raise ValueError(
                    "Stream config does not pass the `type` for validation."
                )

            groups: dict[str, Any] = {}
            grout_dir: Path
            for grout_dir in d.iterdir():
                if grout_dir.is_dir() and (
                    match := Re.RE_GROUP.search(grout_dir.name)
                ):
                    match_data: dict[str, Any] = match.groupdict()
                    groups[match_data["name"]] = {
                        "processes": get_processes_from_path(
                            grout_dir,
                            stream_name=name,
                            group_name=match_data["name"],
                            ignore=ignore,
                        ),
                        **match_data,
                    }

            stream_data["groups"] = groups
            return stream_data

    raise FileNotFoundError(f"Does not found stream: {name!r} at {path}")


def get_processes_from_path(
    path: Path,
    stream_name: str,
    group_name: str,
    ignore: Optional[list[str]] = None,
) -> DictData:
    """Get all process from an input config path.

    :param path: (Path) A config path.
    :param stream_name: (str) A stream name.
    :param group_name: (str) A group name.
    :param ignore: A list of ignore
    """
    process: dict[str, Any] = {}
    for file in path.rglob("*"):

        if file.is_file() and file.suffix in (".yml", ".yaml"):

            if is_ignored(file, ignore):
                continue

            data = YamlEnvFl(path=file).read()
            if data:
                for name in data:
                    process[name] = {
                        "name": name,
                        "group_name": group_name,
                        "stream_name": stream_name,
                        **data[name],
                    }
    return process


def get_process(name: str, path: Path) -> DictData:
    """Get Process data from an input name and path values.

    :param name: (str)
    :param path: (Path)

    :rtype: dict[str, Any]
    """
    ignore = read_ignore(path / ".confignore")
    for file in path.rglob("*"):

        if file.is_file() and file.stem == name:

            if is_ignored(file, ignore):
                continue

            if file.suffix in (".yml", ".yaml"):
                data = YamlEnvFl(path=file).read()
                if name not in data:
                    raise NotImplementedError

                return {
                    "name": name,
                    "group_name": file.parent.name,
                    "stream_name": file.parent.parent.name,
                    **data[name],
                }

            else:
                raise NotImplementedError(
                    f"Get process file: {file.name} does not support for file"
                    f"type: {file.suffix}."
                )
    raise FileNotFoundError(f"{path}/**/{name}.yml")
