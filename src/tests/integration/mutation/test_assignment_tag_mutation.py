from modules.course_template.domain.models.assignment_tag import AssignmentTemplateTag
from tests.utils import authenticated_request, gid


def test_create_assignment_template_tag_mutation(
    db_session,
    graphql_client,
    user_factory,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
    tag_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    tag = tag_factory(name="DML")

    query = """
        mutation createAssignmentTemplateTag($assignmentTemplateId: ID!, $tagId: ID!){
            createAssignmentTemplateTag(assignmentTemplateId: $assignmentTemplateId, tagId: $tagId){
                assignmentTemplateTag{
                    tag{
                        name
                    }
                }
            }
        }
    """
    variables = {"assignmentTemplateId": gid(assignment_template), "tagId": gid(tag)}
    expected = {
        "createAssignmentTemplateTag": {
            "assignmentTemplateTag": {"tag": {"name": tag.name}}
        }
    }

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    tag_templates = db_session.query(AssignmentTemplateTag)
    assert not response.get("errors")
    assert response["data"] == expected
    assert tag_templates.count() == 1


def test_remove_assignment_template_tag_mutation(
    db_session,
    graphql_client,
    user_factory,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
    assignment_template_tag_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    assignment_tag = assignment_template_tag_factory(
        assignment_template=assignment_template
    )

    query = """
        mutation removeAssignmentTemplateTag($assignmentTemplateTagId: ID!){
            removeAssignmentTemplateTag(assignmentTemplateTagId: $assignmentTemplateTagId){
                isRemoved
            }
        }
    """
    variables = {"assignmentTemplateTagId": gid(assignment_tag)}
    expected = {"removeAssignmentTemplateTag": {"isRemoved": True}}

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    tag_templates = db_session.query(AssignmentTemplateTag)
    assert not response.get("errors")
    assert response["data"] == expected
    assert tag_templates.count() == 0
