from graphene import ID, Field, List, Mutation, ObjectType, String

from api.graphql_api.authentication import authentication_required
from api.graphql_api.schema.table_row import TableRowAssignmentTemplateNode
from api.graphql_api.utils import retrieve_id
from modules.course_template.application.services.data_template_service import (
    DataAssignmentTemplateManagementService,
)


class CreateTableAssignmentRow(Mutation):
    row = Field(TableRowAssignmentTemplateNode)

    class Arguments:
        table_assignment_template_id = ID(required=True)
        row_data = List(of_type=List(of_type=String))

    @authentication_required()
    def mutate(
        self,
        info,
        table_assignment_template_id: str,
        row_data: list[list[str]],
        **kwargs
    ):
        session = info.context["session"]
        table_assignment_template_pk = retrieve_id(table_assignment_template_id)
        manager = DataAssignmentTemplateManagementService(session)
        row = manager.create(table_assignment_template_pk, row_data, **kwargs)
        return CreateTableAssignmentRow(row=row)


class TableDataMutation(ObjectType):
    create_table_assignment_row = CreateTableAssignmentRow.Field()
