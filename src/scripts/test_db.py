import base64

from sqlalchemy import MetaData, create_engine
from sqlalchemy_schemadisplay import create_schema_graph

# TODO: Do we need cache=shared in our case?
# engine = create_engine("sqlite:///file:memdb1?mode=memory&cache=shared")

engine = create_engine("sqlite:///:memory:")
metadata = MetaData(bind=engine)
connection = engine.raw_connection()
cursor = connection.cursor()

cursor.execute("""PRAGMA foreign_keys=on;""")
cursor.execute("""DROP TABLE IF EXISTS COMPANY""")
cursor.execute(
    """CREATE TABLE COMPANY
         (ID INT PRIMARY KEY     NOT NULL,
         SUB_ID         TEXT     NOT NULL,
         NAME           TEXT    NOT NULL,
         AGE            INT     NOT NULL,
         ADDRESS        CHAR(50),
         SALARY         REAL);"""
)

cursor.execute(
    "INSERT INTO COMPANY (ID,SUB_ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (1, 'x', 'Paul', 32, 'California', 20000.00 )"
)

cursor.execute(
    "INSERT INTO COMPANY (ID,SUB_ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (2, 'y', 'Allen', 25, 'Texas', 15000.00 )"
)

cursor.execute(
    "INSERT INTO COMPANY (ID,SUB_ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (3, 'z', 'Teddy', 23, 'Norway', 20000.00 )"
)

cursor.execute(
    "INSERT INTO COMPANY (ID,SUB_ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (4, 'w', 'Mark', 25, 'Rich-Mond ', 65000.00 )"
)

connection.commit()

cursor.execute("""DROP TABLE IF EXISTS TEST""")
cursor.execute(
    """CREATE TABLE TEST(
        ID INT PRIMARY KEY     NOT NULL,
        NAME           TEXT    NOT NULL,
        COMPANY_ID     INT     NULL,
        COMPANY_SUB_ID TEXT     NULL,
        FOREIGN KEY (COMPANY_ID) REFERENCES COMPANY ON DELETE SET NULL
    );"""
)

cursor.execute(
    "INSERT INTO TEST (ID,NAME,COMPANY_ID,COMPANY_SUB_ID) VALUES (1, 'OtherTable1', 1, 'x')"
)
cursor.execute(
    "INSERT INTO TEST (ID,NAME,COMPANY_ID,COMPANY_SUB_ID) VALUES (2, 'OtherTable2', 2, 'y')"
)
cursor.execute(
    "INSERT INTO TEST (ID,NAME,COMPANY_ID,COMPANY_SUB_ID) VALUES (3, 'OtherTable3', 3, 'z')"
)
cursor.execute(
    "INSERT INTO TEST (ID,NAME,COMPANY_ID,COMPANY_SUB_ID) VALUES (4, 'OtherTable4', 4, 'w')"
)

connection.commit()

result = cursor.execute(
    "SELECT c.id, c.name, c.age, t.name FROM COMPANY as c LEFT JOIN TEST as t ON c.ID=t.COMPANY_ID"
)
for row in result:
    print(row)

result = cursor.execute("DELETE FROM COMPANY WHERE ID=1")

print("----------------")

result = cursor.execute(
    "SELECT c.id, c.name, c.age, t.name FROM COMPANY as c LEFT JOIN TEST as t ON c.ID=t.COMPANY_ID"
)
for row in result:
    print(row)

print("----------------")

result = cursor.execute("SELECT * FROM TEST")
for row in result:
    print(row)


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


# Zadania na jutro:
# 1. Opracować i spisać dokładny flow tworzenia assignmentu: struktura, dane etc.


# 2. Przechowywanie danych dla assignmentu, czy generowanie ich w locie?
# Odp: przechowywanie

# 3. Schema per Kurs, Quiz, Assignment?
# Odp: per Quiz


# 4. Zapisywać obrazek do base64
# Odp: można

# 5. mutacja do logowania powinna ustawiać refresh token jako ciasteczko
