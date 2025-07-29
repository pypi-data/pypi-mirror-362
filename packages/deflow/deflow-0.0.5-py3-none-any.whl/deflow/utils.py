import json
from pathlib import Path
from typing import Any, Optional, TypedDict, Union

import yaml
from ddeutil.core import merge_list
from ddeutil.io import YamlEnvFl, is_ignored, read_ignore

from .__types import DictData


class ChildData(TypedDict):
    """Child Data dict type."""

    conf: Union[list[DictData], DictData]
    path: Path
    name: str


class ConfData(TypedDict):
    """Config Data dict type."""

    conf: DictData
    children: list[ChildData]


def check_conf(name: str, path: Path, name_key: str = "name") -> Optional[Path]:
    """Check this config contain the specific name.

    Args:
        name (str):
        path:
        name_key:

    Returns:
        Path: If it contains the config name. It will return None if it does not
            contain.
    """
    if (
        path.is_file()
        and path.stem == "config"
        and path.suffix in (".yaml", ".yml")
    ):
        data: Optional[dict[str, Any]] = yaml.safe_load(path.read_text())
        if not data:
            return None
        elif data.get(name_key, "") == name:
            return path.parent
    return None


def search_conf_parent_path(
    name: str, path: Path, name_key: str = "name"
) -> Path:
    """Search the parent of config path.

    Args:
        name:
        path:
        name_key:

    Returns:

    """
    if path.is_file():
        raise ValueError(
            "Path that want to pull data should be directory not file."
        )

    ignore: list[str] = read_ignore(path / ".confignore")
    conf_dir: Optional[Path] = None
    for _dir in path.glob("*"):
        if _dir.is_file() and _dir.name == ".confignore":
            continue

        if is_ignored(_dir, ignore):
            continue

        if _dir.is_file() and (conf_dir := check_conf(name, _dir, name_key)):
            break

        for file in _dir.rglob("*"):

            if is_ignored(file, ignore):
                continue

            if (
                file.is_dir()
                and file.name == name
                and (lc := [i for i in file.glob("*") if i.stem == "config"])
                and (conf_dir := check_conf(name, lc[0], name_key))
            ):
                break

            if file.is_file() and (conf_dir := check_conf(name, _dir)):
                break

        if conf_dir:
            break

    if not conf_dir:
        raise FileNotFoundError(f"Does not found dir name: {name!r}")
    return conf_dir


def get_data(name: str, path: Path) -> ConfData:
    """Get configuration data that store on an input config path.

    Structure:

        path/
          |-- folder1/
          |-- folder1/
          |-- folder2/
                |-- data/
                     |-- config.yml
                     |-- variable.yml
                     |-- ...
          |-- .confignore

    Args:
        name (str):
        path (Path):
    """
    conf_dir: Path = search_conf_parent_path(name, path)

    # NOTE: merge ignore templates together.
    main_ignore: list[str] = read_ignore(path / ".confignore")
    sub_ignore: list[str] = read_ignore(conf_dir / ".confignore")
    all_ignore: list[str] = list(set(merge_list(main_ignore, sub_ignore)))

    conf_data: Optional[DictData] = None
    metadata: DictData = {"conf_dir": conf_dir, "type": "undefined"}
    child_paths: list[ChildData] = []
    for file in conf_dir.rglob("*"):
        if is_ignored(file, all_ignore):
            continue

        if file.stem == "config":
            conf_data = read_conf(file)
            continue

        if file.stem == "variables":
            continue

        if file.is_dir():
            continue

        child_paths.append(
            {
                "conf": (metadata | read_conf(file)),
                "path": file.relative_to(conf_dir),
                "name": file.stem,
            }
        )

    if not conf_data:
        raise FileNotFoundError("Config file does not exists.")

    return {
        "conf": metadata | conf_data,
        "children": child_paths,
    }


def read_conf(path: Path, pass_env: bool = True) -> DictData:
    """Read configuration function.

    Args:
        path (Path): A config file path.
        pass_env (bool): A flag allow this function pass environ variable before
            reading data from config file.
    """
    if not path.exists():
        raise FileNotFoundError(f"{path} does not exists.")

    if path.suffix in (".yml", ".yaml"):

        data: DictData = (
            YamlEnvFl(path).read()
            if pass_env
            else yaml.safe_load(path.read_text())
        )
        if not data:
            raise NotImplementedError("Config was empty")

        if len(data) > 1:
            return {
                "name": (
                    path.parent.stem if path.stem == "config" else path.stem
                ),
                "created_at": path.lstat().st_ctime,
                "updated_at": path.lstat().st_mtime,
                **data,
            }

        first_key: str = next(iter(data.keys()))
        return {
            "name": first_key,
            "created_at": path.lstat().st_ctime,
            "updated_at": path.lstat().st_mtime,
            **data[first_key],
        }
    elif path.suffix in (".txt", ".sql"):
        data: str = path.read_text(encoding="utf-8")
        return {
            "name": path.stem,
            "created_at": path.lstat().st_ctime,
            "updated_at": path.lstat().st_mtime,
            "raw_data": data,
        }
    elif path.suffix in (".json",):
        data: Union[list[DictData], DictData] = json.loads(path.read_text())
        return {
            "name": path.stem,
            "created_at": path.lstat().st_ctime,
            "updated_at": path.lstat().st_mtime,
            "raw_data": data,
        }

    raise NotImplementedError(
        f"Config file format: {path.suffix!r} does not support yet."
    )
