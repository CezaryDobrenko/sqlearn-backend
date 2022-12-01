from modules.course_template.domain.models.quiz import QuizTemplate
from tests.builders import build_assignment_template_database
from tests.utils import authenticated_request, gid


def test_create_quiz_template_mutation(
    db_session, graphql_client, user_factory, course_template_factory
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    template_title = "DML tutorial quiz"
    template_description = "DML tutorial description"

    query = """
        mutation createQuizTemplate($courseTemplateId: ID!, $title: String!, $description: String){
            createQuizTemplate(courseTemplateId: $courseTemplateId, title: $title, description: $description){
                quizTemplate{
                    title
                    description
                    courseTemplate{
                        name
                    }
                }
            }
        }
    """
    variables = {
        "courseTemplateId": gid(course_template),
        "title": template_title,
        "description": template_description,
    }
    expected = {
        "createQuizTemplate": {
            "quizTemplate": {
                "title": template_title,
                "description": template_description,
                "courseTemplate": {"name": course_template.name},
            }
        }
    }

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    quiz_templates = db_session.query(QuizTemplate)
    assert not response.get("errors")
    assert response["data"] == expected
    assert quiz_templates.count() == 1


def test_update_quiz_template_mutation(
    db_session,
    graphql_client,
    user_factory,
    course_template_factory,
    quiz_template_factory,
):
    user = user_factory()
    course_template = course_template_factory(owner=user)
    quiz_template = quiz_template_factory(course_template=course_template)
    new_quiz_title = "DML tutorial quiz"
    new_quiz_description = "DML tutorial description"

    query = """
        mutation updateQuizTemplate($quizTemplateId: ID!, $title: String, $description: String){
            updateQuizTemplate(quizTemplateId: $quizTemplateId, title: $title, description: $description){
                quizTemplate{
                    title
                    description
                    courseTemplate{
                        name
                    }
                }
            }
        }
    """
    variables = {
        "quizTemplateId": gid(quiz_template),
        "title": new_quiz_title,
        "description": new_quiz_description,
    }
    expected = {
        "updateQuizTemplate": {
            "quizTemplate": {
                "title": new_quiz_title,
                "description": new_quiz_description,
                "courseTemplate": {"name": course_template.name},
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
    assert quiz_template.title == new_quiz_title
    assert quiz_template.description == new_quiz_description


def test_remove_quiz_template_mutation(
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
        mutation removeQuizTemplate($quizTemplateId: ID!){
            removeQuizTemplate(quizTemplateId: $quizTemplateId){
                isRemoved
            }
        }
    """
    variables = {"quizTemplateId": gid(quiz_template)}
    expected = {"removeQuizTemplate": {"isRemoved": True}}

    response = graphql_client.execute(
        query,
        variables=variables,
        context_value={"session": db_session, "request": authenticated_request(user)},
    )

    quiz_templates = db_session.query(QuizTemplate)
    assert not response.get("errors")
    assert response["data"] == expected
    assert quiz_templates.count() == 0
