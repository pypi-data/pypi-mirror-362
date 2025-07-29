# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
"""The Core Tasks module for keeping necessary tasks that use on the caller
stage that config in the workflow template.
"""
from __future__ import annotations

from datetime import datetime
from functools import partial
from typing import Any

from ddeutil.workflow import Result, tag

from ....__types import DictData
from ....conf import dynamic
from .models import Group, Process, Stream

VERSION: str = "v1"
TAG_VERSION_1 = partial(tag, name=VERSION)


def tag_routing(alias: str):
    return TAG_VERSION_1(alias=f"routing-{alias}")


@TAG_VERSION_1(alias="get-start-stream-info")
def get_start_stream_info(
    name: str, result: Result, extras: dict[str, Any]
) -> DictData:
    """Get Stream model information. This function use to validate an input
    stream name that exists on the config path.

    :param name: (str) A stream name
    :param result: (Result) A result dataclass for make logging.
    :param extras: (dict[str, Any]) An extra parameters.

    :rtype: DictData
    """
    result.trace.info(f"Start getting stream: {name!r} info.")
    stream: Stream = Stream.from_conf(
        name=name, path=dynamic("deflow_conf_path", extras=extras)
    )
    result.trace.info(
        f"... Start Stream Info:"
        f"||=> freq: {stream.freq.model_dump(by_alias=True)}"
        f"||=> data_freq: {stream.data_freq.model_dump(by_alias=True)}"
    )

    return {
        "name": stream.name,
        "freq": stream.freq.model_dump(by_alias=True),
        "data_freq": stream.data_freq.model_dump(by_alias=True),
        "priority-groups": sorted(stream.priority_group().keys()),
        "stream": stream.model_dump(by_alias=True),
        "audit-date": datetime(2025, 4, 1, 1),
        "logical-date": datetime(2025, 4, 1, 1),
    }


@TAG_VERSION_1(alias="get-groups-from-priority")
def get_groups_from_priority(
    priority: int, stream: Stream, result: Result
) -> DictData:
    """Get groups from priority.

    :param priority: (int) A priority number of groups.
    :param stream: (str) A stream data model.
    :param result: (Result) A result dataclass for make logging.
    """
    result.trace.info(f"Get groups from priority: {priority}")
    groups: list[Group] = [
        group.name for group in stream.priority_group().get(priority)
    ]
    result.trace.info(
        f"Return groups from priority: {priority}||Groups: {groups}||"
    )
    return {"groups": groups}


@TAG_VERSION_1(alias="get-processes-from-group")
def get_processes_from_group(
    group: str, stream: str, result: Result, extras: dict[str, Any]
) -> DictData:
    """Get all process name from a specific group.

    :param group: (str) A group name.
    :param stream: (str) A stream name.
    :param result: (Result) A result dataclass for make logging.
    :param extras: (dict[str, Any]) An extra parameters.
    """
    result.trace.info(
        f"Get processes from group: {group!r} and stream: {stream!r}"
    )
    stream: Stream = Stream.from_conf(
        name=stream, path=dynamic("deflow_conf_path", extras=extras)
    )
    group_model: Group = stream.group(group)
    processes: list[str] = list(group_model.processes)
    result.trace.info(
        f"... Return process from group: {group!r}||Processes: {processes}||"
    )
    return {
        "processes": processes,
        "group": group_model.model_dump(by_alias=True),
        "stream": stream.model_dump(by_alias=True),
    }


@TAG_VERSION_1(alias="start-process")
def start_process(
    name: str, result: Result, extras: dict[str, Any]
) -> DictData:
    """Start process with an input process name.

    :param name: (str) A process name.
    :param result: (Result) A result dataclass for make logging.
    :param extras: (dict[str, Any]) An extra parameters.
    """
    result.trace.info(f"Start getting process: {name!r} info")
    process: Process = Process.from_path(
        name=name, path=dynamic("deflow_conf_path", extras=extras)
    )
    result.trace.info(f"... routing of this process: {process.routing}")
    return {
        "routing": process.routing,
        "process": process.model_dump(by_alias=True),
    }
