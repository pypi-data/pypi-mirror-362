import copy
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field
from typing_extensions import Self

from ....__types import DictData
from ....utils import ConfData, get_data
from ...models import AbstractModel
from .utils import get_node, get_node_assets


class NodeDeps(BaseModel):
    name: str
    trigger_rule: Optional[str] = Field(default=None)


class Node(BaseModel):
    """Node model.

        The node model will represent the minimum action for ETL/ELT/EL or
    trigger or hook external API/SDK.
    """

    conf_dir: Path = Field(description="A dir path of this config data.")
    name: str = Field(description="A node name.")
    pipeline_name: Optional[str] = Field(
        default=None, description="A pipeline name of this node."
    )
    desc: Optional[str] = Field(default=None)
    upstream: list[NodeDeps] = Field(default_factory=list)
    operator: str = Field(description="An node operator.")
    task: str = Field(description="A node task.")
    params: dict[str, Any] = Field(default_factory=dict)
    assets: list[str] = Field(default_factory=list)

    @classmethod
    def from_conf(cls, name: str, path: Path) -> Self:
        """Construct Node model from an input node name and config path."""
        data: DictData = get_node(name=name, path=path)

        if (t := data.pop("type")) != cls.__name__:
            raise ValueError(f"Type {t!r} does not match with {cls}")

        loader_data: DictData = copy.deepcopy(data)
        return cls.model_validate(obj=loader_data)

    def asset(self, name: str) -> DictData:
        """Get the asset data with a specific name.

        :param name: (str) An asset name that want to load from the config path.
        """
        if name not in self.assets:
            raise ValueError(f"This asset, {name!r}, does not exists.")
        return get_node_assets(name, path=self.conf_dir)

    def sync_assets(self) -> DictData:
        """Return mapping of its asset name and asset data from the conf path.

        :rtype: DictData
        """
        return {
            asset_name: self.asset(asset_name) for asset_name in self.assets
        }


class Lineage(BaseModel):
    inlets: list[NodeDeps] = Field(default_factory=list)
    outlets: list[NodeDeps] = Field(default_factory=list)


class Pipeline(AbstractModel):
    """Pipeline model."""

    name: str = Field(description="A pipeline name.")
    desc: Optional[str] = Field(
        default=None,
        description=(
            "A pipeline description that allow to write with markdown syntax."
        ),
    )
    nodes: dict[str, Node] = Field(
        default_factory=list, description="A list of Node model."
    )

    @classmethod
    def load_conf(cls, name: str, path: Path) -> Self:
        """Load configuration data."""
        load_data: ConfData = get_data(name, path=path)

        nodes: dict[str, Node] = {}
        for child in load_data["children"]:
            if child["conf"].get("type", "") != "Node":
                continue
            node = Node.model_validate(child["conf"])
            nodes[node.name] = node

        return cls.model_validate(
            obj={
                "nodes": nodes,
                **load_data["conf"],
            }
        )

    def node(self, name: str) -> Node:
        """Get the Node model with pass the specific node name."""
        return self.nodes[name]

    def node_priorities(self) -> list[list[str]]:
        """Generate the Node priorities that convert from its upstream field.

        :rtype: list[list[str]]
        """

        if not self.nodes:
            return []

        # Build reverse adjacency list and in-degree count in one pass
        in_degree: dict[str, int] = {}
        dependents = {}  # node -> [nodes that depend on it]

        # Initialize
        for node in self.nodes:
            in_degree[node] = 0
            dependents[node] = []

        # Build graph
        for node, config in self.nodes.items():
            if config.upstream:
                for upstream in config.upstream:
                    upstream_name = upstream.name

                    # Add upstream node if not seen before
                    if upstream_name not in in_degree:
                        in_degree[upstream_name] = 0
                        dependents[upstream_name] = []

                    # Update relationships
                    in_degree[node] += 1
                    dependents[upstream_name].append(node)

        # NOTE: Kahn's algorithm with level-by-level processing
        result: list[list[str]] = []
        current_level: list[str] = [
            node for node, degree in in_degree.items() if degree == 0
        ]

        while current_level:

            # NOTE: For consistent output
            current_level.sort()

            # NOTE: Shallow copy
            result.append(current_level[:])

            next_level: list[str] = []
            for node in current_level:

                # NOTE: Decrease in-degree for all dependents
                for dependent in dependents[node]:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        next_level.append(dependent)

            current_level = next_level

        # Cycle detection
        if sum(in_degree.values()) > 0:
            raise ValueError("Circular dependency detected")

        return result

    def lineage(self) -> list[Lineage]: ...
