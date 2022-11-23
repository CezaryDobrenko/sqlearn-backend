from tests.utils import authenticated_request, gid


def test_authorized_node_quiz_templates_query(
    db_session, graphql_client, user_factory, quiz_template_factory
):
    user = user_factory()
    quiz_tempate = quiz_template_factory()

    query = """
        query quizTemplate($id: ID!){
            authorizedNode(id: $id){
                ...on QuizTemplateNode{
                    id
                    title
                }
            }
        }
    """
    variables = {"id": gid(quiz_tempate)}
    expected = {"authorizedNode": None}

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    assert not response.get("errors")
    assert response["data"] == expected


def test_user_course_templates_query(
    db_session,
    graphql_client,
    user_factory,
    course_template_factory,
    quiz_template_factory,
):
    user = user_factory()
    template = course_template_factory(owner=user)
    quiz_1 = quiz_template_factory(
        course_template=template, title="quiz1", description="desc1"
    )
    quiz_2 = quiz_template_factory(
        course_template=template, title="quiz2", description="desc2"
    )

    query = """
        query quizTemplates($id: ID!){
            authorizedNode(id: $id){
                ...on CourseTemplateNode{
                    quizTemplates{
                        edges{
                            node{
                                title
                                description
                            }
                        }
                    }
                }
            }
        }
    """
    variables = {"id": gid(template)}
    expected = {
        "authorizedNode": {
            "quizTemplates": {
                "edges": [
                    {
                        "node": {
                            "title": quiz_1.title,
                            "description": quiz_1.description,
                        }
                    },
                    {
                        "node": {
                            "title": quiz_2.title,
                            "description": quiz_2.description,
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
