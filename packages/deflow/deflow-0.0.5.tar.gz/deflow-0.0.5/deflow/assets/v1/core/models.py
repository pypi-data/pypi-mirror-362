# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import copy
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Literal, Optional
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field
from typing_extensions import Self

from ....__types import DictData
from .utils import get_process, get_stream


class Frequency(BaseModel):
    """Frequency model for generate audit date."""

    type: Literal["daily", "monthly", "yearly", "hourly"] = Field(
        default="daily",
        description="A frequency type.",
    )
    offset: int = Field(
        default=1,
        ge=-100,
        le=100,
        description="An offset value for decrease freq type unit.",
    )

    def gen_datetime(
        self, dt: Optional[datetime] = None, tz: Optional[ZoneInfo] = None
    ) -> datetime:
        """Generate and prepare datetime

        :param dt: (datetime) A datetime object.
        :param tz: (ZoneInfo) A timezone information.
        """
        tz: ZoneInfo = tz or ZoneInfo("UTC")
        if dt is None:
            dt = datetime.now(tz=tz)
        return dt - timedelta(days=self.offset)


class Stream(BaseModel):
    """Stream model is the main model that keep the Group and Process models.
    This model will construct from the config data that extract from YAML file.
    """

    name: str = Field(description="A stream name")
    freq: Frequency = Field(
        default_factory=Frequency,
        description="A frequency",
        alias="frequency",
    )
    data_freq: Frequency = Field(
        default_factory=Frequency,
        description="A data frequency",
        alias="date_frequency",
    )
    groups: dict[str, Group] = Field(
        default_factory=dict,
        description="A mapping of Group model and its name.",
    )
    tags: list[str] = Field(default_factory=list)

    @classmethod
    def from_conf(cls, name: str, path: Path) -> Self:
        """Construct Stream model from an input stream name and config path.

        :param name: (str) A stream name that want to search from config path.
        :param path: (Path) A config path.

        :rtype: Self
        """
        data: DictData = get_stream(name=name, path=path)

        if (t := data.pop("type")) != cls.__name__:
            raise ValueError(f"Type {t!r} does not match with {cls}")

        loader_data: DictData = copy.deepcopy(data)
        loader_data["name"] = name
        return cls.model_validate(obj=loader_data)

    def group(self, name: str) -> Group:
        """Get a Group model by name.

        :param name: (str) A group name.

        :rtype: Group
        """
        return self.groups[name]

    def priority_group(self) -> dict[int, list[Group]]:
        """Return the ordered list of distinct group priority that keep in this
        stream.

        :rtype: dict[int, list[Group]]
        """
        rs: dict[int, list[Group]] = {}
        for group in self.groups.values():
            if group.priority in rs:
                rs[group.priority].append(group)
            else:
                rs[group.priority] = [group]
        return rs


GroupTier = Literal[
    "raw", "bronze", "silver", "gold", "staging", "operation", "platinum"
]


class Group(BaseModel):
    """Group model that use for grouping process together and run with its
    priority.
    """

    name: str = Field(description="A group name")
    tier: GroupTier = Field(description="A tier of this group.")
    priority: int = Field(gt=0, description="A priority of this group.")
    processes: dict[str, Process] = Field(
        default_factory=dict,
        description="A list of Process model.",
    )

    @property
    def filename(self) -> str:
        """Return the file name that combine name, tier, and priority of this
        group.

        :rtype: str
        """
        return f"{self.name}.{self.tier}.{self.priority}"

    def process(self, name: str) -> Process:
        """Return Process model with an input specific name.

        :param name: (str) A process string name that want to get Process model.

        :rtype: Process
        """
        return self.processes[name]


class Dependency(BaseModel):
    """Dependency model"""

    name: str = Field(description="A dependency process name.")
    offset: int = Field(default=1, description="A dependency offset.")


class Connection(BaseModel):
    """Connection model."""

    ir: Optional[str] = Field(default=None)
    service: str
    host: str
    database: str
    user: str
    secret: Optional[str] = Field(
        default=None,
        description="A secret key for getting from any secret manager service.",
    )


class TestDataset(BaseModel):
    """Test Dataset model for keeping pointer of dummy or sampling file for
    testing run the workflow on the local before deploy to target environment.
    """

    file: Optional[str] = Field(
        default=None,
        description="A test filename.",
    )


class Dataset(BaseModel):
    """Dataset model."""

    conn: str = Field(alias="conn", description="A connection name.")
    scm: str = Field(
        alias="schema",
        description="A schema or parent path name.",
    )
    tbl: str = Field(alias="table", description="A table or file name.")
    tests: TestDataset = Field(
        default_factory=TestDataset,
        description=(
            "A test pointer for sync testing data that use for unittest."
        ),
    )


class Process(BaseModel):
    """Process model for only one action for move the data from source to
    target with routing type.

    Note:

        Process ==> Source --> Transform --> Target
    """

    name: str = Field(description="A process name.")
    stream: Optional[str] = Field(default=None, description="A stream name.")
    group: Optional[str] = Field(default=None, description="A group name.")
    routing: int = Field(
        ge=1, lt=20, description="A routing value for running workflow."
    )
    load_type: str = Field(description="A loading type.")
    priority: int = Field(gt=0, description="A priority of this process.")
    source: Dataset
    target: Dataset
    extras: dict[str, Any] = Field(default_factory=dict)
    deps: list[Dependency] = Field(
        default_factory=list,
        description="List of process dependency.",
    )

    @classmethod
    def from_path(cls, name: str, path: Path) -> Self:
        """Get Process instance from the config path."""
        data = get_process(name=name, path=path)

        if (t := data.pop("type")) != cls.__name__:
            raise ValueError(f"Type {t!r} does not match with {cls}")

        loader_data: DictData = copy.deepcopy(data)
        return cls.model_validate(obj=loader_data)


class Dates(BaseModel):
    """Dates model."""

    audit_date: datetime = Field(
        description=(
            "An audit datetime that will equal the current release date."
        )
    )
    logical_date: datetime = Field(
        description=(
            "A logical date that will generate from the frequency object."
        )
    )
