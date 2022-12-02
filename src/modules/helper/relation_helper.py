from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from instance_access import has_user_access
from models import User
from modules.course_template.domain.models.column import TableColumnAssignmentTemplate
from modules.course_template.domain.models.relation import (
    TableRelationAssignmentTemplate,
)
from modules.course_template.domain.models.table import TableAssignmentTemplate
from modules.database_preset.domain.models.column import TableColumn
from modules.database_preset.domain.models.relation import TableRelation
from modules.database_preset.domain.models.table import Table

TABLE_MODEL = Table | TableAssignmentTemplate
COLUMN_MODEL = TableColumn | TableColumnAssignmentTemplate
RELATION_MODEL = TableRelation | TableRelationAssignmentTemplate


def get_relation_value(relation: RELATION_MODEL, value: str, **kwargs) -> str:
    return kwargs[value] if value in kwargs else getattr(relation, value)


def is_relation_exist(
    session: Session, relation_model: RELATION_MODEL, column: COLUMN_MODEL
) -> bool:
    relations = (
        session.query(relation_model)
        .filter(
            or_(
                and_(
                    relation_model.table_id == column.assigned_table_id,
                    relation_model.table_column_name == column.name,
                ),
                and_(
                    relation_model.relation_table_id == column.assigned_table_id,
                    relation_model.relation_column_name == column.name,
                ),
            )
        )
        .all()
    )
    return True if relations else False


def is_relation_valid(
    session: Session,
    model: TABLE_MODEL,
    table_id: int,
    column_name: str,
    user: User,
) -> bool:
    table = session.query(model).get(table_id)
    if has_user_access(table, user):
        return True if table.has_column(column_name) else False
    raise Exception("Permision Denied")


def is_relation_already_defined(
    session: Session,
    model: RELATION_MODEL,
    source_table_id: int,
    source_column: str,
    relation_table_id: int,
    relation_column: str,
) -> bool:
    is_already_defined = (
        session.query(model)
        .filter(
            model.table_column_name == source_column,
            model.table_id == source_table_id,
            model.relation_column_name == relation_column,
            model.relation_table_id == relation_table_id,
        )
        .first()
    )
    return True if is_already_defined else False
