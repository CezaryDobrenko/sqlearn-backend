import base64

from sqlalchemy import MetaData, create_engine
from sqlalchemy_schemadisplay import create_schema_graph

# TODO: Do we need cache=shared in our case?
# engine = create_engine("sqlite:///file:memdb1?mode=memory&cache=shared")

engine = create_engine("sqlite:///:memory:")
metadata = MetaData(bind=engine)
connection = engine.raw_connection()
cursor = connection.cursor()

cursor.execute("""DROP TABLE IF EXISTS COMPANY""")
cursor.execute(
    """CREATE TABLE COMPANY
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         AGE            INT     NOT NULL,
         ADDRESS        CHAR(50),
         SALARY         REAL);"""
)

cursor.execute(
    "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (1, 'Paul', 32, 'California', 20000.00 )"
)

cursor.execute(
    "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (2, 'Allen', 25, 'Texas', 15000.00 )"
)

cursor.execute(
    "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )"
)

cursor.execute(
    "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )"
)

connection.commit()

cursor.execute("""DROP TABLE IF EXISTS TEST""")
cursor.execute(
    """CREATE TABLE TEST
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         COMPANY_ID     INT     NOT NULL,
         FOREIGN KEY (COMPANY_ID) REFERENCES COMPANY);"""
)

cursor.execute("INSERT INTO TEST (ID,NAME,COMPANY_ID) VALUES (1, 'OtherTable1', 1)")
cursor.execute("INSERT INTO TEST (ID,NAME,COMPANY_ID) VALUES (2, 'OtherTable2', 2)")
cursor.execute("INSERT INTO TEST (ID,NAME,COMPANY_ID) VALUES (3, 'OtherTable3', 3)")
cursor.execute("INSERT INTO TEST (ID,NAME,COMPANY_ID) VALUES (4, 'OtherTable4', 4)")

connection.commit()

graph = create_schema_graph(
    metadata=metadata,
    show_datatypes=True,
    show_indexes=False,
    rankdir="LR",
    concentrate=False,
    relation_options={
        "fontsize": "7",
        "style": "bold",
        "labeldistance": 3,
        "minlen": 3,
    },
)
graph.write_png("scripts/test_db.png")
connection.close()

png = graph.create_png()
encoded_png = base64.b64encode(png)
print(encoded_png)


# Zadania na jutro:
# 1. Opracować i spisać dokładny flow tworzenia assignmentu: struktura, dane etc.


# 2. Przechowywanie danych dla assignmentu, czy generowanie ich w locie?
# Odp: przechowywanie

# 3. Schema per Kurs, Quiz, Assignment?
# Odp: per Quiz


# 4. Zapisywać obrazek do base64
# Odp: można

# 5. mutacja do logowania powinna ustawiać refresh token jako ciasteczko
