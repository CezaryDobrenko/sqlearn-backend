from sqlalchemy.orm import Session

from modules.database_preset.domain.models.relation import RelationAction


class RowActionService:
    session: Session
    on_delete: bool
    on_update: bool
    update_values: dict

    def __init__(
        self, session: Session, on_delete: bool = False, on_update: bool = False
    ):
        if on_update and on_delete:
            raise Exception("Select either on_delete or on_update action")

        self.session = session
        self.on_delete = on_delete
        self.on_update = on_update

    def execute_on_delete(self, row) -> bool:
        for relation in row.table_assignment_template.related_by:
            for source_cell in self._get_cells(row, relation):
                for related_cell in self._get_related_cells(source_cell, relation):
                    if relation.action == RelationAction.CASCADE:
                        self._cascade_action(related_cell, source_cell)

                    if relation.action == RelationAction.SET_DEFAULT:
                        self._set_default_action(related_cell, relation)

                    if relation.action == RelationAction.SET_NULL:
                        self._set_null_action(related_cell)

                    if relation.action == RelationAction.NO_ACTION:
                        self._no_action(relation)
        return True

    def _no_action(self, relation):
        """
        Execute "NO ACTION" Relation rule
        """

        raise Exception(f"Relation: {relation.name} violated")

    def _cascade_action(self, related_cell, source_cell):
        """
        Execute "DELETE CASCADE" Relation rule
        """

        if self.on_delete:
            related_row = self._get_row(related_cell)
            self.execute_on_delete(related_row)
            self.session.delete(related_row)

        if self.on_update:
            related_cell.value = source_cell.value

    def _set_null_action(self, related_cell):
        """
        Execute "SET NULL" Relation rule
        """

        related_column = self._get_column(related_cell)
        if related_column.is_null:
            related_cell.set_null_value()
        else:
            raise Exception(f"Column: {related_column.name} is not nullable")

    def _set_default_action(self, related_cell, relation):
        """
        Execute "SET DEFAULT" Relation rule
        """

        related_column = self._get_column(related_cell)
        default_value = related_column.default_value
        is_unique = relation.source_column.is_unique
        is_defined = relation.relation_column.is_value_already_defined(default_value)
        if is_defined and is_unique:
            raise Exception(
                f"Column: {related_column.name} is unique. Cannot insert another default value"
            )
        if is_defined:
            related_cell.set_default_value()
        else:
            raise Exception(
                f"Column: {related_column.name} doesn't contain default value"
            )

    def _get_cells(self, row, relation) -> list:
        """
        Returns cells from table related to other table
        """

        return [
            cell
            for cell in row.cells
            if cell.table_column_assignment_template == relation.relation_column
        ]

    def _get_related_cells(self, source_cell, relation) -> list:
        """
        Returns cells from related table connected to source cell
        """

        return [
            related_cell
            for related_cell in relation.source_column.data
            if source_cell.value == related_cell.value
        ]

    def _get_row(self, related_cell):
        return related_cell.table_row_assignment_template

    def _get_column(self, related_cell):
        return related_cell.table_column_assignment_template
