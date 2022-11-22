from sqlalchemy_schemadisplay import create_schema_graph

from models.base_model import metadata

graph = create_schema_graph(
    metadata=metadata,
    show_datatypes=True,
    show_indexes=False,
    rankdir="TB",
    concentrate=False,
    relation_options={
        "fontsize": "7",
        "style": "bold",
        "labeldistance": 3,
        "minlen": 3,
    },
)
graph.write_png("../spec/dbschema.png")
