from flask import Flask, request
from flask_cors import CORS
from graphene_file_upload.flask import FileUploadGraphQLView
from sqlalchemy.orm import scoped_session, sessionmaker

from api.graphql_api import schema
from config import Config
from models.base_model import engine

app = Flask(__name__)


if Config.DEBUG:
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
else:
    CORS(app, resources={r"/*": {"origins": "*"}})

Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
db_session = scoped_session(Session)

app.add_url_rule(
    "/graphql/",
    view_func=FileUploadGraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True,
        get_context=lambda: {"session": db_session, "request": request},
    ),
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=Config.DEBUG)
