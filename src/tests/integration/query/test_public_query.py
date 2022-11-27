def test_public_avalible_courses_query(
    db_session, graphql_client, user_factory, course_template_factory
):
    user = user_factory()
    _ = course_template_factory(
        name="template_1", is_public=True, is_published=False, owner=user
    )
    _ = course_template_factory(
        name="template_2", is_public=False, is_published=True, owner=user
    )
    other_user = user_factory()
    tempate = course_template_factory(
        name="template_3", is_public=True, is_published=True, owner=other_user
    )
    _ = course_template_factory(
        name="template_4", is_public=False, is_published=False, owner=other_user
    )

    query = """
        query public{
            public{
                avalibleCourses{
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
        "public": {
            "avalibleCourses": {
                "edges": [
                    {
                        "node": {
                            "name": tempate.name,
                            "description": tempate.description,
                            "isPublic": tempate.is_public,
                            "isPublished": tempate.is_published,
                        }
                    },
                ]
            }
        }
    }

    response = graphql_client.execute(
        query,
        context_value={"session": db_session},
    )

    assert not response.get("errors")
    assert response["data"] == expected


def test_public_databases_query(
    db_session, graphql_client, user_factory, database_factory
):
    database_1 = database_factory(name="database_1", user=None)
    database_2 = database_factory(name="database_2", user=None)
    user = user_factory()
    _ = database_factory(name="database_3", user=user)
    other_user = user_factory()
    _ = database_factory(name="database_4", user=other_user)

    query = """
        query publicDatabases{
            public{
                databases{
                    edges{
                        node{
                            name
                        }
                    }
                }
            }
        }
    """
    expected = {
        "public": {
            "databases": {
                "edges": [
                    {
                        "node": {
                            "name": database_1.name,
                        }
                    },
                    {
                        "node": {
                            "name": database_2.name,
                        }
                    },
                ]
            }
        }
    }

    response = graphql_client.execute(query, context_value={"session": db_session})

    assert not response.get("errors")
    assert response["data"] == expected


def test_public_tags_query(db_session, graphql_client, tag_factory):
    tag_1 = tag_factory(name="DCL")
    tag_2 = tag_factory(name="DQL")
    tag_3 = tag_factory(name="DML")
    tag_4 = tag_factory(name="DDL")

    query = """
        query publicTags{
            public{
                tags{
                    edges{
                        node{
                            name
                        }
                    }
                }
            }
        }
    """
    expected = {
        "public": {
            "tags": {
                "edges": [
                    {"node": {"name": tag_1.name}},
                    {"node": {"name": tag_2.name}},
                    {"node": {"name": tag_3.name}},
                    {"node": {"name": tag_4.name}},
                ]
            }
        }
    }

    response = graphql_client.execute(query, context_value={"session": db_session})

    assert not response.get("errors")
    assert response["data"] == expected
