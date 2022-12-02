from modules.course_template.domain.models.relation import (
    TableRelationAssignmentTemplate,
)
from modules.database_preset.domain.models.relation import RelationAction, TableRelation
from tests.builders import (
    build_assignment_template,
    build_assignment_template_database,
    build_assignment_template_table,
)
from tests.utils import authenticated_request, gid


def test_create_table_relation_mutation(
    db_session,
    graphql_client,
    user_factory,
    database_factory,
    table_factory,
    table_column_factory,
):
    user = user_factory()
    database = database_factory(user=user)
    users_table = table_factory(database=database, name="users")
    _ = table_column_factory(table=users_table, name="id")
    _ = table_column_factory(table=users_table, name="name")
    cars_table = table_factory(database=database, name="cars")
    _ = table_column_factory(table=cars_table, name="id")
    _ = table_column_factory(table=cars_table, name="name")
    _ = table_column_factory(table=cars_table, name="user_id")

    name = "new_fk"
    action = "CASCADE"
    table_id = gid(users_table)
    table_column_name = "id"
    relation_table_id = gid(cars_table)
    relation_column_name = "user_id"

    query = """
        mutation createTableRelation(
            $name: String!,
            $action: String!,
            $sourceColumnName: String!,
            $sourceTableId: ID!,
            $relationColumnName: String!,
            $relationTableId: ID!,
        ){
            createTableRelation(
                name: $name,
                action: $action,
                sourceColumnName: $sourceColumnName,
                sourceTableId: $sourceTableId,
                relationColumnName: $relationColumnName,
                relationTableId: $relationTableId,
            ){
                relation{
                    name
                    action
                    tableColumnName
                    table{
                        name
                    }
                    relationColumnName
                    relationTable{
                        name
                    }
                }
            }
        }
    """
    variables = {
        "name": name,
        "action": action,
        "sourceTableId": table_id,
        "sourceColumnName": table_column_name,
        "relationTableId": relation_table_id,
        "relationColumnName": relation_column_name,
    }
    expected = {
        "createTableRelation": {
            "relation": {
                "name": name,
                "action": action,
                "tableColumnName": table_column_name,
                "table": {"name": users_table.name},
                "relationColumnName": relation_column_name,
                "relationTable": {"name": cars_table.name},
            }
        }
    }

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    relations = db_session.query(TableRelation)
    assert not response.get("errors")
    assert response["data"] == expected
    assert relations.count() == 1


def test_update_table_relation_mutation(
    db_session,
    graphql_client,
    user_factory,
    database_factory,
    table_factory,
    table_relation_factory,
    table_column_factory,
):
    user = user_factory()
    database = database_factory(user=user)
    users_table = table_factory(database=database, name="users")
    _ = table_column_factory(table=users_table, name="id")
    _ = table_column_factory(table=users_table, name="name")
    paintings_table = table_factory(database=database, name="paintings")
    _ = table_column_factory(table=paintings_table, name="id")
    _ = table_column_factory(table=paintings_table, name="name")
    _ = table_column_factory(table=paintings_table, name="user_id")
    cars_table = table_factory(database=database, name="cars")
    _ = table_column_factory(table=cars_table, name="id")
    _ = table_column_factory(table=cars_table, name="name")
    _ = table_column_factory(table=cars_table, name="user_id")
    _ = table_column_factory(table=cars_table, name="painting_id")

    relation = table_relation_factory(
        name="old_fk",
        action="SET_NULL",
        table=users_table,
        table_column_name="id",
        relation_table=paintings_table,
        relation_column_name="user_id",
    )
    new_name = "new_fk"
    new_action = "CASCADE"
    new_table_id = gid(paintings_table)
    new_table_column_name = "id"
    new_relation_table_id = gid(cars_table)
    new_relation_column_name = "painting_id"

    query = """
        mutation updateTableRelation(
            $tableRelationId: ID!,
            $name: String,
            $action: String,
            $sourceColumnName: String,
            $sourceTableId: ID,
            $relationColumnName: String,
            $relationTableId: ID,
        ){
            updateTableRelation(
                tableRelationId: $tableRelationId,
                name: $name,
                action: $action,
                sourceColumnName: $sourceColumnName,
                sourceTableId: $sourceTableId,
                relationColumnName: $relationColumnName,
                relationTableId: $relationTableId,
            ){
                relation{
                    name
                    action
                    tableColumnName
                    table{
                        name
                    }
                    relationColumnName
                    relationTable{
                        name
                    }
                }
            }
        }
    """
    variables = {
        "tableRelationId": gid(relation),
        "name": new_name,
        "action": new_action,
        "sourceColumnName": new_table_column_name,
        "sourceTableId": new_table_id,
        "relationColumnName": new_relation_column_name,
        "relationTableId": new_relation_table_id,
    }
    expected = {
        "updateTableRelation": {
            "relation": {
                "name": new_name,
                "action": new_action,
                "tableColumnName": new_table_column_name,
                "table": {"name": paintings_table.name},
                "relationColumnName": new_relation_column_name,
                "relationTable": {"name": cars_table.name},
            }
        }
    }

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    assert not response.get("errors")
    assert response["data"] == expected
    assert relation.name == new_name
    assert relation.action == RelationAction.CASCADE
    assert relation.table == paintings_table
    assert relation.table_column_name == new_table_column_name
    assert relation.relation_table == cars_table
    assert relation.relation_column_name == new_relation_column_name


def test_remove_table_relation_mutation(
    db_session,
    graphql_client,
    user_factory,
    database_factory,
    table_factory,
    table_relation_factory,
):
    user = user_factory()
    database = database_factory(user=user)
    table = table_factory(database=database, name="users")
    relation = table_relation_factory(table=table)

    query = """
        mutation removeTableRelation($tableRelationId: ID!){
            removeTableRelation(tableRelationId: $tableRelationId){
                isRemoved
            }
        }
    """
    variables = {"tableRelationId": gid(relation)}
    expected = {"removeTableRelation": {"isRemoved": True}}

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    relations = db_session.query(TableRelation)
    assert not response.get("errors")
    assert response["data"] == expected
    assert relations.count() == 0


def test_create_table_relation_assignment_template_mutation(
    db_session, graphql_client, user_factory
):
    user = user_factory()
    assignment_template = build_assignment_template(user)
    database_template = build_assignment_template_database(assignment_template)
    other_table = build_assignment_template_table(database_template)
    _, related_table, _ = database_template.tables.all()

    name = "new_fk"
    action = "CASCADE"
    table_id = gid(related_table)
    table_column_name = "id"
    relation_table_id = gid(other_table)
    relation_column_name = "id"

    query = """
        mutation createTableRelationAssignmentTemplate(
            $name: String!,
            $action: String!,
            $sourceColumnName: String!,
            $sourceTableId: ID!,
            $relationColumnName: String!,
            $relationTableId: ID!,
        ){
            createTableRelationAssignmentTemplate(
                name: $name,
                action: $action,
                sourceColumnName: $sourceColumnName,
                sourceTableId: $sourceTableId,
                relationColumnName: $relationColumnName,
                relationTableId: $relationTableId,
            ){
                relation{
                    name
                    action
                    tableColumnName
                    table{
                        name
                    }
                    relationColumnName
                    relationTable{
                        name
                    }
                }
            }
        }
    """
    variables = {
        "name": name,
        "action": action,
        "sourceTableId": table_id,
        "sourceColumnName": table_column_name,
        "relationTableId": relation_table_id,
        "relationColumnName": relation_column_name,
    }
    expected = {
        "createTableRelationAssignmentTemplate": {
            "relation": {
                "name": name,
                "action": action,
                "tableColumnName": table_column_name,
                "table": {"name": related_table.name},
                "relationColumnName": relation_column_name,
                "relationTable": {"name": other_table.name},
            }
        }
    }

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    relations = db_session.query(TableRelationAssignmentTemplate)
    assert not response.get("errors")
    assert response["data"] == expected
    assert relations.count() == 2


def test_update_table_relation_assignment_template_mutation(
    db_session, graphql_client, user_factory
):
    user = user_factory()
    assignment_template = build_assignment_template(user)
    database_template = build_assignment_template_database(assignment_template)
    other_table = build_assignment_template_table(database_template)
    source_table, related_table, _ = database_template.tables.all()
    relation = source_table.relations.first()
    new_name = "new_fk"
    new_action = "CASCADE"
    new_table_id = gid(related_table)
    new_table_column_name = "id"
    new_relation_table_id = gid(other_table)
    new_relation_column_name = "id"

    query = """
        mutation updateTableRelationAssignmentTemplate(
            $relationAssignmentTemplateId: ID!,
            $name: String,
            $action: String,
            $sourceColumnName: String,
            $sourceTableId: ID,
            $relationColumnName: String,
            $relationTableId: ID,
        ){
            updateTableRelationAssignmentTemplate(
                relationAssignmentTemplateId: $relationAssignmentTemplateId,
                name: $name,
                action: $action,
                sourceColumnName: $sourceColumnName,
                sourceTableId: $sourceTableId,
                relationColumnName: $relationColumnName,
                relationTableId: $relationTableId,
            ){
                relation{
                    name
                    action
                    tableColumnName
                    table{
                        name
                    }
                    relationColumnName
                    relationTable{
                        name
                    }
                }
            }
        }
    """
    variables = {
        "relationAssignmentTemplateId": gid(relation),
        "name": new_name,
        "action": new_action,
        "sourceColumnName": new_table_column_name,
        "sourceTableId": new_table_id,
        "relationColumnName": new_relation_column_name,
        "relationTableId": new_relation_table_id,
    }
    expected = {
        "updateTableRelationAssignmentTemplate": {
            "relation": {
                "name": new_name,
                "action": new_action,
                "tableColumnName": new_table_column_name,
                "table": {"name": related_table.name},
                "relationColumnName": new_relation_column_name,
                "relationTable": {"name": other_table.name},
            }
        }
    }

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    relations = db_session.query(TableRelationAssignmentTemplate)
    assert not response.get("errors")
    assert response["data"] == expected
    assert relation.name == new_name
    assert relation.action == RelationAction.CASCADE
    assert relation.table == related_table
    assert relation.table_column_name == new_table_column_name
    assert relation.relation_table == other_table
    assert relation.relation_column_name == new_relation_column_name
    assert relations.count() == 1


def test_remove_table_relation_assignment_template_mutation(
    db_session, graphql_client, user_factory
):
    user = user_factory()
    assignment_template = build_assignment_template(user)
    database_template = build_assignment_template_database(assignment_template)
    table, _ = database_template.tables.all()
    relation = table.relations.first()

    query = """
        mutation removeTableRelationAssignmentTemplate($relationAssignmentTemplateId: ID!){
            removeTableRelationAssignmentTemplate(relationAssignmentTemplateId: $relationAssignmentTemplateId){
                isRemoved
            }
        }
    """
    variables = {"relationAssignmentTemplateId": gid(relation)}
    expected = {"removeTableRelationAssignmentTemplate": {"isRemoved": True}}

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    relations = db_session.query(TableRelationAssignmentTemplate)
    assert not response.get("errors")
    assert response["data"] == expected
    assert relations.count() == 0
