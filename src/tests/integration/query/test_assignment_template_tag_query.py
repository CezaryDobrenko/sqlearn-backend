from tests.utils import authenticated_request, gid


def test_authorized_node_assignment_template_tags_query(
    db_session, graphql_client, user_factory, assignment_template_tag_factory
):
    user = user_factory()
    assignment_tempate_tag = assignment_template_tag_factory()

    query = """
        query assignmentTemplateTag($id: ID!){
            authorizedNode(id: $id){
                ...on AssignmentTemplateTagNode{
                    id
                    tag{
                        name
                    }
                }
            }
        }
    """
    variables = {"id": gid(assignment_tempate_tag)}
    expected = {"authorizedNode": None}

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    assert not response.get("errors")
    assert response["data"] == expected


def test_user_assignment_template_tags_query(
    db_session,
    graphql_client,
    user_factory,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
    tag_factory,
    assignment_template_tag_factory,
):
    user = user_factory()
    template = course_template_factory(owner=user)
    quiz = quiz_template_factory(course_template=template)
    assignment = assignment_template_factory(quiz_template=quiz)
    _ = assignment_template_tag_factory(
        assignment_template=assignment, tag=tag_factory(name="DML")
    )
    _ = assignment_template_tag_factory(
        assignment_template=assignment, tag=tag_factory(name="DCL")
    )
    _ = assignment_template_tag_factory(
        assignment_template=assignment, tag=tag_factory(name="DDL")
    )

    query = """
        query assignmentTemplateTag($id: ID!){
            authorizedNode(id: $id){
                ...on AssignmentTemplateNode{
                    templateTags{
                        edges{
                            node{
                                tag{
                                    name
                                }
                            }
                        }
                    }
                }
            }
        }
    """
    variables = {"id": gid(assignment)}
    expected = {
        "authorizedNode": {
            "templateTags": {
                "edges": [
                    {"node": {"tag": {"name": "DML"}}},
                    {"node": {"tag": {"name": "DCL"}}},
                    {"node": {"tag": {"name": "DDL"}}},
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
