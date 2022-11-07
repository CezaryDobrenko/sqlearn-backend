from flask import Flask, request, session
from flask_cors import CORS
from flask_graphql import GraphQLView
from sqlalchemy.orm import scoped_session, sessionmaker

from api.graphql_api import schema
from config import Config
from models.base_model import engine

app = Flask(__name__)
app.config["SECRET_KEY"] = "very_secret_key"


if Config.DEBUG:
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
else:
    CORS(app, resources={r"/*": {"origins": "*"}})

Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
db_session = scoped_session(Session)


class MyCustomGraphQLView(GraphQLView):
    def dispatch_request(self):
        response = super(MyCustomGraphQLView, self).dispatch_request()

        cookie_session = self.get_context().get("cookie_session")
        if "set_cookie" in cookie_session:
            response.headers["Set-Cookie"] = cookie_session.get("set_cookie")
        cookie_session.clear()

        return response


def graphql_view():
    view = MyCustomGraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True,
        get_context=lambda: {
            "session": db_session,
            "request": request,
            "cookie_session": session,
        },
    )
    return view


app.add_url_rule("/graphql/", view_func=graphql_view(), methods=["POST", "GET"])


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=Config.DEBUG)
