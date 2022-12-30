from sqlalchemy.orm import Session

from modules.database_preset.domain.models.relation import RelationAction


class RowActionService:
    session: Session
    on_delete: bool
    on_update: bool
    update_values: dict

    def __init__(
        self,
        session: Session,
        on_delete: bool = False,
        on_update: bool = False,
        **kwargs,
    ):
        if on_update and on_delete:
            raise Exception("Select either on_delete or on_update action")

        self.session = session
        self.on_delete = on_delete
        self.on_update = on_update
        self.update_values = kwargs

    def execute_on_delete(self, row) -> bool:
        for relation in row.table_assignment_template.related_by:
            for source_cell in self._get_cells(row, relation):
                for related_cell in self._get_related_cells(source_cell, relation):
                    related_cell_key = f"{related_cell.id}"
                    related_row = self._get_row(related_cell)
                    related_column = self._get_column(related_cell)
                    default_value = related_column.default_value

                    self.execute_on_delete(related_row)

                    if relation.action == RelationAction.CASCADE:
                        self.update_values[related_cell_key] = None
                        self._delete_cascade_action(related_row)

                    if relation.action == RelationAction.SET_DEFAULT:
                        if not self._is_referenced_value_exist(relation, default_value):
                            raise Exception(
                                f"Related Column: {related_column.name} doesn't contain default value"
                            )
                        self.update_values[related_cell_key] = default_value
                        self._set_default_action(related_cell, relation)

                    if relation.action == RelationAction.SET_NULL:
                        self.update_values[related_cell_key] = None
                        self._set_null_action(related_cell, relation)

                    if relation.action == RelationAction.NO_ACTION:
                        self._no_action(relation)
        return True

    def execute_on_update(self, row) -> bool:
        for relation in row.table_assignment_template.related_by:
            for source_cell in self._get_cells(row, relation):
                if f"{source_cell.id}" in self.update_values.keys():
                    for related_cell in self._get_related_cells(source_cell, relation):
                        related_cell_key = f"{related_cell.id}"
                        source_cell_key = f"{source_cell.id}"
                        related_row = self._get_row(related_cell)
                        related_column = self._get_column(related_cell)
                        default_value = related_column.default_value
                        self.update_values[related_cell_key] = self.update_values[
                            source_cell_key
                        ]

                        self.execute_on_update(related_row)

                        if relation.action == RelationAction.CASCADE:
                            self._update_cascade_action(
                                related_cell, source_cell, relation
                            )

                        if relation.action == RelationAction.SET_DEFAULT:
                            if not self._is_referenced_value_exist(
                                relation, default_value
                            ):
                                raise Exception(
                                    f"Related Column: {related_column.name} doesn't contain default value"
                                )
                            self.update_values[related_cell_key] = default_value
                            self._set_default_action(related_cell, relation)

                        if relation.action == RelationAction.SET_NULL:
                            self.update_values[related_cell_key] = None
                            self._set_null_action(related_cell, relation)

                        if relation.action == RelationAction.NO_ACTION:
                            self._no_action(relation)
        return True

    def _is_referenced_value_exist(self, relation, default_value):
        """
        Compare persistent database data with data not yet saved in update_values dict
        """
        possible_values = []
        for cell in relation.relation_column.data:
            if f"{cell.id}" in self.update_values.keys():
                possible_values.append(self.update_values.get(f"{cell.id}"))
            else:
                possible_values.append(cell.value)

        if default_value in possible_values:
            return True
        return False

    def _no_action(self, relation):
        """
        Execute "NO ACTION" Relation rule
        """
        raise Exception(f"Relation: {relation.name} violated")

    def _delete_cascade_action(self, related_row):
        """
        Execute "DELETE CASCADE" Relation rule
        """

        self.session.delete(related_row)

    def _update_cascade_action(self, related_cell, source_cell, relation):
        """
        Execute "UPDATE CASCADE" Relation rule
        """

        new_value = self.update_values[f"{source_cell.id}"]
        if new_value is None:
            self._set_null_action(related_cell, relation)
        else:
            related_cell.value = new_value

    def _set_null_action(self, related_cell, relation):
        """
        Execute "SET NULL" Relation rule
        """

        related_column = self._get_column(related_cell)
        if related_column.is_autoincrement:
            related_cell.set_value()
        elif related_column.is_null:
            related_cell.set_null_value()
        else:
            raise Exception(
                f"Column: {related_column.name} is not nullable. Relation: {relation.name} violated"
            )

    def _set_default_action(self, related_cell, relation):
        """
        Execute "SET DEFAULT" Relation rule
        """

        related_column = self._get_column(related_cell)
        if relation.source_column.is_unique:
            raise Exception(
                f"Column: {related_column.name} is unique. Cannot insert another default value"
            )
        if relation.source_column.is_autoincrement:
            related_cell.set_value()
        related_cell.set_default_value()

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
