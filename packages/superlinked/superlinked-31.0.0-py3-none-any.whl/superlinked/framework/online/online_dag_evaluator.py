# Copyright 2024 Superlinked, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from functools import partial

import structlog
from beartype.typing import Mapping, Sequence

from superlinked.framework.common.dag.context import ExecutionContext
from superlinked.framework.common.dag.dag import Dag
from superlinked.framework.common.dag.dag_effect import DagEffect
from superlinked.framework.common.dag.node import Node
from superlinked.framework.common.dag.schema_dag import SchemaDag
from superlinked.framework.common.data_types import Vector
from superlinked.framework.common.exception import (
    InvalidDagEffectException,
    InvalidSchemaException,
)
from superlinked.framework.common.parser.parsed_schema import (
    ParsedSchema,
    ParsedSchemaWithEvent,
)
from superlinked.framework.common.schema.id_schema_object import IdSchemaObject
from superlinked.framework.common.schema.schema_object import SchemaObject
from superlinked.framework.common.storage_manager.storage_manager import StorageManager
from superlinked.framework.common.telemetry.telemetry_registry import telemetry
from superlinked.framework.compiler.online.online_schema_dag_compiler import (
    OnlineSchemaDagCompiler,
)
from superlinked.framework.online.dag.evaluation_result import EvaluationResult
from superlinked.framework.online.dag.online_schema_dag import OnlineSchemaDag
from superlinked.framework.online.dag_effect_group import DagEffectGroup

logger = structlog.get_logger()


class OnlineDagEvaluator:
    def __init__(
        self,
        dag: Dag,
        schemas: set[SchemaObject],
        storage_manager: StorageManager,
    ) -> None:
        super().__init__()
        self._dag = dag
        self._schemas = schemas
        self._storage_manager = storage_manager
        self._schema_online_schema_dag_mapper = self.__init_schema_online_schema_dag_mapper(
            self._schemas, self._dag, storage_manager
        )
        self._dag_effect_group_to_online_schema_dag = self.__map_dag_effect_group_to_online_schema_dag(self._dag)
        self.__effect_to_group = self.__map_effect_to_group(self._dag_effect_group_to_online_schema_dag)
        self._log_dag_init()

    @property
    def effect_to_group(self) -> Mapping[DagEffect, DagEffectGroup]:
        return self.__effect_to_group

    def _log_dag_init(self) -> None:
        for schema, online_schema_dag in self._schema_online_schema_dag_mapper.items():
            logger.info(
                "initialized entity dag",
                schema=schema._schema_name,
                node_info=[(node.class_name, node.node_id) for node in online_schema_dag.nodes],
            )
        for dag_effect_group, online_schema_dag in self._dag_effect_group_to_online_schema_dag.items():
            logger.info(
                "initialized event dag",
                affected_schema=dag_effect_group.affected_schema._schema_name,
                affecting_schema=dag_effect_group.affecting_schema._schema_name,
                node_info=[(node.class_name, node.node_id) for node in online_schema_dag.nodes],
            )

    def __get_single_schema(self, parsed_schemas: Sequence[ParsedSchema]) -> IdSchemaObject:
        unique_schemas: set[IdSchemaObject] = {parsed_schema.schema for parsed_schema in parsed_schemas}
        if len(unique_schemas) != 1:
            raise InvalidSchemaException(
                f"Multiple schemas ({[s._schema_name for s in unique_schemas]}) present in the index."
            )
        return next(iter(unique_schemas))

    def evaluate(
        self,
        parsed_schemas: Sequence[ParsedSchema],
        context: ExecutionContext,
    ) -> list[EvaluationResult[Vector] | None]:
        index_schema = self.__get_single_schema(parsed_schemas)
        if (online_schema_dag := self._schema_online_schema_dag_mapper.get(index_schema)) is not None:
            with telemetry.span(
                "dag.evaluate",
                attributes={"schema": index_schema._schema_name, "n_entities": len(parsed_schemas), "is_event": False},
            ):
                results = online_schema_dag.evaluate(parsed_schemas, context)
            logger_to_use = logger.bind(schema=index_schema._schema_name)
            logger_to_use.info("evaluated entities", n_entities=len(results))
            for i, result in enumerate(results):
                logger_to_use.debug(
                    "evaluated entity",
                    pii_vector=partial(str, result.main.value) if result is not None else "None",
                    pii_field_values=[field.value for field in parsed_schemas[i].fields],
                )
            return results

        raise InvalidSchemaException(f"Schema ({index_schema._schema_name}) isn't present in the index.")

    def evaluate_by_dag_effect_group(
        self,
        parsed_schema_with_events: Sequence[ParsedSchemaWithEvent],
        context: ExecutionContext,
        dag_effect_group: DagEffectGroup,
    ) -> list[EvaluationResult[Vector] | None]:
        if (online_schema_dag := self._dag_effect_group_to_online_schema_dag.get(dag_effect_group)) is not None:
            labels = {
                "schema": dag_effect_group.affected_schema._schema_name,
                "n_entities": len(parsed_schema_with_events),
                "is_event": True,
            }
            with telemetry.span("dag.evaluate", attributes=labels):
                results = online_schema_dag.evaluate(parsed_schema_with_events, context)
            logger.info("evaluated events", n_records=len(results))
            return results
        raise InvalidDagEffectException(f"DagEffectGroup ({dag_effect_group}) isn't present in the index.")

    def __init_schema_online_schema_dag_mapper(
        self,
        schemas: set[SchemaObject],
        dag: Dag,
        storage_manager: StorageManager,
    ) -> dict[SchemaObject, OnlineSchemaDag]:
        return {
            schema: OnlineSchemaDagCompiler(set(dag.nodes)).compile_schema_dag(
                dag.project_to_schema(schema), storage_manager
            )
            for schema in schemas
        }

    def __map_dag_effect_group_to_online_schema_dag(self, dag: Dag) -> dict[DagEffectGroup, OnlineSchemaDag]:
        return {
            dag_effect_group: self.__compile_online_schema_dag(dag, dag_effect_group)
            for dag_effect_group in DagEffectGroup.group_similar_effects(dag.dag_effects)
        }

    def __compile_online_schema_dag(self, dag: Dag, dag_effect_group: DagEffectGroup) -> OnlineSchemaDag:
        nodes = self.__get_nodes_for_effect_group(dag, dag_effect_group)
        schema_dag = SchemaDag(dag_effect_group.event_schema, list(nodes))
        return OnlineSchemaDagCompiler(nodes).compile_schema_dag(schema_dag, self._storage_manager)

    def __get_nodes_for_effect_group(self, dag: Dag, dag_effect_group: DagEffectGroup) -> set[Node]:
        return {node for effect in dag_effect_group.effects for node in self.__get_nodes_for_effect(dag, effect)}

    def __get_nodes_for_effect(self, dag: Dag, dag_effect: DagEffect) -> set[Node]:
        nodes_to_visit: list[Node] = [dag.index_node]
        visited_nodes: set[Node] = set()
        while nodes_to_visit:
            current_node = nodes_to_visit.pop()
            visited_nodes.add(current_node)
            parent_nodes = current_node.project_parents_for_dag_effect(dag_effect)
            nodes_to_visit.extend(node for node in parent_nodes if node not in visited_nodes)
        return visited_nodes

    def __map_effect_to_group(
        self, dag_effect_group_to_online_schema_dag: Mapping[DagEffectGroup, OnlineSchemaDag]
    ) -> dict[DagEffect, DagEffectGroup]:
        return {effect: group for group in dag_effect_group_to_online_schema_dag for effect in group.effects}
