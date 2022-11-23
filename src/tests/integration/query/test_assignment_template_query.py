from tests.utils import authenticated_request, gid


def test_authorized_node_assignment_templates_query(
    db_session, graphql_client, user_factory, assignment_template_factory
):
    user = user_factory()
    assignment_tempate = assignment_template_factory()

    query = """
        query assignmentTemplate($id: ID!){
            authorizedNode(id: $id){
                ...on AssignmentTemplateNode{
                    id
                    title
                }
            }
        }
    """
    variables = {"id": gid(assignment_tempate)}
    expected = {"authorizedNode": None}

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    assert not response.get("errors")
    assert response["data"] == expected


def test_user_assignment_templates_query(
    db_session,
    graphql_client,
    user_factory,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
):
    user = user_factory()
    template = course_template_factory(owner=user)
    quiz = quiz_template_factory(course_template=template)
    assignment_1 = assignment_template_factory(
        quiz_template=quiz, title="assignment_1", description="desc_1", ordinal=1
    )
    assignment_3 = assignment_template_factory(
        quiz_template=quiz, title="assignment_3", description="desc_3", ordinal=3
    )
    assignment_2 = assignment_template_factory(
        quiz_template=quiz, title="assignment_2", description="desc_2", ordinal=2
    )

    query = """
        query assignmentTemplate($id: ID!){
            authorizedNode(id: $id){
                ...on QuizTemplateNode{
                    assignmentsTemplates{
                        edges{
                            node{
                                title
                                description
                                ordinal
                            }
                        }
                    }
                }
            }
        }
    """
    variables = {"id": gid(quiz)}
    expected = {
        "authorizedNode": {
            "assignmentsTemplates": {
                "edges": [
                    {
                        "node": {
                            "title": assignment_1.title,
                            "description": assignment_1.description,
                            "ordinal": assignment_1.ordinal,
                        }
                    },
                    {
                        "node": {
                            "title": assignment_2.title,
                            "description": assignment_2.description,
                            "ordinal": assignment_2.ordinal,
                        }
                    },
                    {
                        "node": {
                            "title": assignment_3.title,
                            "description": assignment_3.description,
                            "ordinal": assignment_3.ordinal,
                        }
                    },
                ]
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
