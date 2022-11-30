import datetime

from modules.course_template.domain.models.course import CourseTemplate
from tests.utils import authenticated_request, gid
from tests.builders import build_assignment_template_database


def test_create_course_template_mutation(db_session, graphql_client, user_factory):
    user = user_factory()
    template_name = "DML tutorial course"
    template_description = "DML tutorial description"

    query = """
        mutation createCourseTemplate($name: String!, $description: String){
            createCourseTemplate(name: $name, description: $description){
                courseTemplate{
                    name
                    description
                    ownerId
                }
            }
        }
    """
    variables = {"name": template_name, "description": template_description}
    expected = {
        "createCourseTemplate": {
            "courseTemplate": {
                "name": template_name,
                "description": template_description,
                "ownerId": gid(user),
            }
        }
    }

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    courses = db_session.query(CourseTemplate)
    assert not response.get("errors")
    assert response["data"] == expected
    assert courses.count() == 1


def test_update_course_template_mutation(
    db_session, graphql_client, user_factory, course_template_factory
):
    user = user_factory()
    course_template = course_template_factory(
        owner=user, name="old_name", description="old_description", is_published=True
    )
    new_template_name = "DML tutorial course"
    new_template_description = "DML tutorial description"

    query = """
        mutation updateCourseTemplate($courseTemplateId: ID!, $name: String, $description: String){
            updateCourseTemplate(courseTemplateId: $courseTemplateId, name: $name, description: $description){
                courseTemplate{
                    name
                    description
                    ownerId
                }
            }
        }
    """
    variables = {
        "courseTemplateId": gid(course_template),
        "name": new_template_name,
        "description": new_template_description,
    }
    expected = {
        "updateCourseTemplate": {
            "courseTemplate": {
                "name": new_template_name,
                "description": new_template_description,
                "ownerId": gid(user),
            }
        }
    }

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    assert not response.get("errors")
    assert response["data"] == expected
    assert course_template.name == new_template_name
    assert course_template.description == new_template_description
    assert course_template.is_published is False
    assert course_template.last_update_at.strftime("%Y-%m-%d %H:%M") == now


def test_remove_course_template_mutation(
    db_session,
    graphql_client,
    user_factory,
    course_template_factory,
    quiz_template_factory,
    assignment_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    assignment_template = assignment_template_factory(quiz_template=quiz_template)
    build_assignment_template_database(assignment_template)

    query = """
        mutation removeCourseTemplate($courseTemplateId: ID!){
            removeCourseTemplate(courseTemplateId: $courseTemplateId){
                isRemoved
            }
        }
    """
    variables = {"courseTemplateId": gid(course_template)}
    expected = {"removeCourseTemplate": {"isRemoved": True}}

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    course_templates = db_session.query(CourseTemplate)
    assert not response.get("errors")
    assert response["data"] == expected
    assert course_templates.count() == 0


def test_publish_course_template_mutation(
    db_session, graphql_client, user_factory, course_template_factory
):
    user = user_factory()
    course_template = course_template_factory(owner=user, is_published=False)

    query = """
        mutation publishCourseTemplate($courseTemplateId: ID!){
            publishCourseTemplate(courseTemplateId: $courseTemplateId){
                isPublished
            }
        }
    """
    variables = {"courseTemplateId": gid(course_template)}
    expected = {"publishCourseTemplate": {"isPublished": True}}

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    course_template = db_session.query(CourseTemplate).first()
    assert not response.get("errors")
    assert response["data"] == expected
    assert course_template.is_published is True


def test_withdraw_course_template_mutation(
    db_session, graphql_client, user_factory, course_template_factory
):
    user = user_factory()
    course_template = course_template_factory(owner=user, is_published=True)

    query = """
        mutation withdrawCourseTemplate($courseTemplateId: ID!){
            withdrawCourseTemplate(courseTemplateId: $courseTemplateId){
                isWithdrawed
            }
        }
    """
    variables = {"courseTemplateId": gid(course_template)}
    expected = {"withdrawCourseTemplate": {"isWithdrawed": True}}

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    course_template = db_session.query(CourseTemplate).first()
    assert not response.get("errors")
    assert response["data"] == expected
    assert course_template.is_published is False
