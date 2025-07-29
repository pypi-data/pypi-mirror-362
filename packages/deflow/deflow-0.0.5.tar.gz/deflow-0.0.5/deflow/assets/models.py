"""Abstract model module that will use for all framework core model for
uniqueness of abstraction that will make it easy to implement and optimize.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from typing import Any, Callable, Literal

from ddeutil.workflow import get_dt_now
from pydantic import BaseModel, Field
from pydantic.functional_validators import field_validator
from typing_extensions import Self

from ..__types import DictData

RunMode = Literal["N", "R", "F", "T"]
GetConfigFunc = Callable[[str, Path], DictData]


class AbstractModel(BaseModel, ABC):
    """Abstract model for any data framework model."""

    conf_dir: Path = Field(description="A dir path of this config data.")
    name: str = Field(description="A config name.")
    type: str = Field(
        description="A type of config. It should be the same as model name."
    )
    desc: str = Field(
        default=None,
        description=(
            "A description of this config that allow writing with the markdown "
            "syntax."
        ),
    )
    created_at: datetime = Field(
        default_factory=get_dt_now,
        description=(
            "A created datetime of this config data when loading from " "file."
        ),
    )
    updated_at: datetime = Field(
        default_factory=get_dt_now,
        description=(
            "A updated datetime of this config data when loading from " "file."
        ),
    )
    tags: list[str] = Field(
        default_factory=list,
        description="A list of tag for simple group this config.",
    )

    @field_validator("desc", mode="after")
    def __dedent_desc__(cls, data: str) -> str:
        """Prepare description string that was created on a template.

        Args:
            data: A description string value that want to dedent.

        Returns:
            str: The de-dented description string.
        """
        return dedent(data.lstrip("\n"))

    @classmethod
    @abstractmethod
    def load_conf(cls, name: str, path: Path) -> DictData:
        """Load config

        :param name: (str) A pipeline name that want to search from config path.
        :param path: (Path) A config path.

        :rtype: ConfData
        """

    @classmethod
    def from_conf(cls, name: str, path: Path) -> Self:
        """Construct model from an input config name and searching path.

        :param name: (str) A config name that want to search from path.
        :param path: (Path) A searching path to find this specific config name.
        :return:
        """
        return cls.model_validate(obj=cls.load_conf(name, path=path))

    def get_variable(self, env: str) -> DictData:
        """Get variable data from this config directory."""
        import yaml

        variable = Variable.model_validate(
            obj=yaml.safe_load((self.conf_dir / "variables.yml").open())
        )
        return variable.get_env(env)


class Variable(BaseModel):
    """Variable model."""

    type: Literal["Variable"]
    stages: dict[str, dict[str, Any]] = Field(default_factory=dict)

    def get_env(self, env: str) -> DictData:
        """Get environment variable data."""
        if env not in self.stages:
            raise ValueError(
                f"Stage environment: {env!r} does not set on this "
                f"variable file."
            )
        return self.stages[env]
