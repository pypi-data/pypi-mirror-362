# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import os
from pathlib import Path
from typing import Final, Optional, TypeVar

from .__types import DictData

PREFIX: Final[str] = "DEFLOW"
ASSETS_PATH: Final[Path] = Path(__file__).parent / "assets"
T = TypeVar("T")


def env(
    var: str, default: Optional[str] = None
) -> Optional[str]:  # pragma: no cov
    """Get the specific environment variable with the project prefix.

    :param var: An environment variable name.
    :param default: A default value if it does not exist.

    :rtype: str | None
    """
    return os.getenv(f"{PREFIX}_{var.upper().replace(' ', '_')}", default)


class Config:
    """Config object."""

    @property
    def deflow_conf_path(self) -> Path:
        return Path(env("CORE_CONF_PATH", "./conf"))

    @property
    def deflow_registry_caller(self) -> list[str]:
        regis_call_str: str = env("CORE_REGISTRY_CALLER", ".")
        return [r.strip() for r in regis_call_str.split(",")]

    @property
    def version(self) -> str:
        return env("CORE_VERSION", "v1")

    @property
    def env(self) -> str:
        return env("CORE_ENV", "test")


config = Config()


def dynamic(
    key: Optional[str] = None,
    *,
    f: Optional[T] = None,
    extras: Optional[DictData] = None,
) -> Optional[T]:
    """Dynamic get config if extra value was passed at run-time.

    :param key: (str) A config key that get from Config object.
    :param f: (T) An inner config function scope.
    :param extras: An extra values that pass at run-time.

    :rtype: T
    """
    extra: Optional[T] = (extras or {}).get(key, None)
    conf: Optional[T] = getattr(config, key, None) if f is None else f
    if extra is None:
        return conf
    if not isinstance(extra, type(conf)):
        raise TypeError(
            f"Type of config {key!r} from extras: {extra!r} does not valid "
            f"as config {type(conf)}."
        )
    return extra
