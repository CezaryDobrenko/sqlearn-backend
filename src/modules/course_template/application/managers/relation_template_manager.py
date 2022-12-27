from exceptions import RelationException
from modules.course_template.domain.models.relation import (
    TableRelationAssignmentTemplate,
)
from modules.course_template.domain.models.table import TableAssignmentTemplate
from modules.helper.relation_helper import (
    get_relation_value,
    is_relation_already_defined,
    is_relation_valid,
)


class TableRelationAssignmentTemplateManager:
    def __init__(self, session):
        self.session = session

    def can_create(
        self,
        source_table_id: int,
        source_column_name: str,
        relation_table_id: int,
        relation_column_name: str,
        **kwargs
    ) -> bool:
        is_relation_defined = is_relation_already_defined(
            self.session,
            TableRelationAssignmentTemplate,
            source_table_id,
            source_column_name,
            relation_table_id,
            relation_column_name,
        )
        if not is_relation_defined:
            user = kwargs["current_user"]
            is_source_table_valid = is_relation_valid(
                self.session,
                TableAssignmentTemplate,
                source_table_id,
                source_column_name,
                user,
            )
            is_relation_table_valid = is_relation_valid(
                self.session,
                TableAssignmentTemplate,
                relation_table_id,
                relation_column_name,
                user,
            )
            if not is_source_table_valid:
                raise RelationException("Source column invalid!")
            if not is_relation_table_valid:
                raise RelationException("Destination column invalid!")

            # TODO: Add validation if defined data is acceptable for relation

            return True
        raise RelationException("Relation already defined!")

    def can_update(self, relation: TableRelationAssignmentTemplate, **kwargs) -> bool:
        source_table_id = get_relation_value(relation, "table_id", **kwargs)
        source_column = get_relation_value(relation, "table_column_name", **kwargs)
        relation_table_id = get_relation_value(relation, "relation_table_id", **kwargs)
        relation_column = get_relation_value(relation, "relation_column_name", **kwargs)

        if (
            relation.relation_column_name == relation_column
            and relation.relation_table_id == relation_table_id
            and relation.table_column_name == source_column
            and relation.table_id == source_table_id
        ):
            return True

        return self.can_create(
            source_table_id,
            source_column,
            relation_table_id,
            relation_column,
            **{"current_user": kwargs["current_user"]}
        )
