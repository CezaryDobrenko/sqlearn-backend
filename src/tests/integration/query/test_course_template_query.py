from tests.utils import authenticated_request, gid


def test_authorized_node_course_templates_query(
    db_session, graphql_client, user_factory, course_template_factory
):
    user = user_factory()
    tempate_1 = course_template_factory(
        name="template_1", is_public=True, is_published=False, owner=user
    )

    query = """
        query courseTemplate($id: ID!){
            authorizedNode(id: $id){
                ...on CourseTemplateNode{
                    id
                    name
                    description
                    isPublic
                    isPublished
                }
            }
        }
    """
    variables = {"id": gid(tempate_1)}
    expected = {"authorizedNode": None}

    response = graphql_client.execute(
        query, variables=variables, context_value={"session": db_session, "request": {}}
    )

    assert not response.get("errors")
    assert response["data"] == expected


def test_user_course_templates_query(
    db_session, graphql_client, user_factory, course_template_factory
):
    user = user_factory()
    tempate_1 = course_template_factory(
        name="template_1", is_public=True, is_published=False, owner=user
    )
    tempate_2 = course_template_factory(
        name="template_2", is_public=False, is_published=True, owner=user
    )
    other_user = user_factory()
    _ = course_template_factory(name="template_3", owner=other_user)

    query = """
        query user{
            user{
                courseTemplates{
                    edges{
                        node{
                            name
                            description
                            isPublic
                            isPublished
                        }
                    }
                }
            }
        }
    """
    expected = {
        "user": {
            "courseTemplates": {
                "edges": [
                    {
                        "node": {
                            "name": tempate_1.name,
                            "description": tempate_1.description,
                            "isPublic": tempate_1.is_public,
                            "isPublished": tempate_1.is_published,
                        }
                    },
                    {
                        "node": {
                            "name": tempate_2.name,
                            "description": tempate_2.description,
                            "isPublic": tempate_2.is_public,
                            "isPublished": tempate_2.is_published,
                        }
                    },
                ]
            }
        }
    }

    response = graphql_client.execute(
        query,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    assert not response.get("errors")
    assert response["data"] == expected
