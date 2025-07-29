# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Union

from ddeutil.io import YamlEnvFl, is_ignored, read_ignore

from ....__types import DictData, ListData


def get_pipeline(name: str, path: Path) -> DictData:
    """Get Pipeline data that store on an input config path.

    :param name: A pipeline name that want to search and extract data from the
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
                    f"Get pipeline file: {cfile.name} does not exist."
                )

            data: DictData = YamlEnvFl(path=cfile).read()
            if name not in data:
                raise ValueError(
                    f"Pipeline config does not set {name!r} config data."
                )
            elif "type" not in (pipeline_data := data[name]):
                raise ValueError(
                    "Pipeline config does not pass the `type` for validation."
                )

            nodes: dict[str, Any] = {}
            f: Path
            for f in d.rglob("*"):
                if not f.is_file():
                    continue

                if is_ignored(f, ignore):
                    continue

                if f.suffix not in (".yml", ".yaml"):
                    continue

                node_data = YamlEnvFl(path=f).read()
                if node_data:
                    for nn in node_data:

                        if not (t := node_data[nn].get("type")) or t != "Node":
                            continue

                        nodes[nn] = {
                            "name": nn,
                            "pipeline_name": name,
                            "conf_dir": d,
                            **node_data[nn],
                        }

            pipeline_data["nodes"] = nodes
            pipeline_data["conf_dir"] = d
            return pipeline_data

    raise FileNotFoundError(f"Does not found pipeline: {name!r} at {path}")


def get_node_assets(name: str, path: Path) -> Union[DictData, ListData]:
    """Get the node asset data from a specific path."""
    data: Union[DictData, ListData] = {}
    if (file := (path / name)).exists():
        if file.is_dir():
            raise NotImplementedError(
                f"Asset location does not support for dir type, {file}."
            )

        if file.suffix in (".yml", ".yaml"):
            data = YamlEnvFl(path=file).read()
        elif file.suffix in (".json",):
            data = json.loads(file.read_text(encoding="utf-8"))
        elif file.suffix in (".sql", ".txt"):
            data["raw_text"] = file.read_text(encoding="utf-8")
        else:
            raise NotImplementedError(
                f"Asset file format does not support yet, {file}. "
                f"For the currently, it already support for `json`, `yaml`, "
                f"and `sql` file formats."
            )

    return data


def get_node(name: str, path: Path) -> DictData:
    ignore = read_ignore(path / ".confignore")
    for file in path.rglob("*"):

        if file.is_file() and file.stem == name:

            if is_ignored(file, ignore):
                continue

            if file.suffix in (".yml", ".yaml"):
                data = YamlEnvFl(path=file).read()
                if name != data.get("name", ""):
                    raise NotImplementedError

                return {
                    "name": name,
                    "pipeline_name": file.parent.name,
                    "conf_dir": file.parent,
                    **data,
                }

            else:
                raise NotImplementedError(
                    f"Get node file: {file.name} does not support for file"
                    f"type: {file.suffix}."
                )
    raise FileNotFoundError(f"{path}/**/{name}.yml")
