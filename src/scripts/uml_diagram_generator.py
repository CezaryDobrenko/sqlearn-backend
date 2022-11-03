from sqlalchemy_schemadisplay import create_schema_graph

from models.base_model import metadata

graph = create_schema_graph(
    metadata=metadata,
    show_datatypes=True,
    show_indexes=True,
    rankdir="TB",
    concentrate=True,
)
graph.write_png("../spec/dbschema.png")
