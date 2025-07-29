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
from .models import Node, Pipeline

VERSION: str = "v2"
TAG_VERSION_2 = partial(tag, name=VERSION)


@TAG_VERSION_2(alias="get-start-pipeline-info")
def get_start_pipeline_info(
    name: str,
    result: Result,
    extras: dict[str, Any],
) -> DictData:
    """Get Pipeline model information. This function use to validate an input
    pipeline name that exists on the config path.

    :param name: (str) A pipeline name
    :param result: (Result) A result dataclass for make logging.
    :param extras: (dict[str, Any]) An extra parameters.

    :rtype: DictData
    """
    result.trace.info(f"Start get pipeline: {name!r} info.")
    pipeline: Pipeline = Pipeline.from_conf(
        name=name, path=dynamic("deflow_conf_path", extras=extras)
    )
    node_priorities: list[list[str]] = pipeline.node_priorities()

    result.trace.info(
        f"... Start Pipeline Info:||"
        f"> Pipeline name: {pipeline.name!r}||"
        f"> Node priorities: {node_priorities}"
    )
    node_priorities_map: dict[int, list[str]] = dict(enumerate(node_priorities))
    return {
        "name": pipeline.name,
        "stream": pipeline.model_dump(by_alias=True),
        "audit-date": datetime(2025, 4, 1, 1),
        "logical-date": datetime(2025, 4, 1, 1),
        "node-priorities-key": list(node_priorities_map.keys()),
        "node-priorities": node_priorities_map,
    }


@TAG_VERSION_2(alias="start-node")
def start_node(
    name: str,
    result: Result,
    extras: dict[str, Any],
) -> DictData:
    """Get Node model information and start node with an input process name.

    :param name: (str) A process name.
    :param result: (Result) A result dataclass for make logging.
    :param extras: (dict[str, Any]) An extra parameters.
    """
    result.trace.info(f"Start get node: {name!r} info")
    node: Node = Node.from_conf(
        name=name, path=dynamic("deflow_conf_path", extras=extras)
    )
    result.trace.info(
        f"... Start Node Info:||"
        f"> Node name: {node.name}||"
        f"> Node operator: {node.operator}||"
        f"> Node task: {node.task}||"
    )
    return {
        "node": node,
        "operator": node.operator,
        "task": node.task,
    }
