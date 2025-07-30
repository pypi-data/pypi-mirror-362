import pytest
import psycopg
from psycopg import sql

from modules.models import DatabaseConnection
from modules.regions import Region
from modules.categories import CATEGORIES


def test_create_database(database):

    assert isinstance(database, DatabaseConnection)


def test_connection_string(database_with_fake_password):

    assert database_with_fake_password.conn_string == "postgresql://doadmin:fakepassword@db-postgresql-ams3-65339-do-user-23767944-0.l.db.ondigitalocean.com:25060/defaultdb?sslmode=require"


def test_database_connection(database):

    assert database.check_connection() == 0


def test_raise_error_database_connection(database_with_fake_password):

    with pytest.raises(psycopg.OperationalError):
        database_with_fake_password.check_connection()


def test_drop_schema(database, schema="test_schema"):
    
    database.drop_schema_cascade(schema)


def test_create_schema(database, schema="test_schema"):
    
    database.create_schema(schema)


def test_create_table(database, schema="test_schema", table="test"):

    with psycopg.connect(conninfo=database.conn_string) as conn:
        with conn.cursor() as cur:

            create_query = sql.SQL("CREATE TABLE {sch_name}.{tbl_name} ({fields})").format(
                sch_name = sql.SQL( schema ),
                tbl_name = sql.SQL( table ),
                fields = sql.SQL( ', ' ).join([sql.SQL("id serial PRIMARY KEY"), sql.SQL("num integer"), sql.SQL("data text")])
                )

            cur.execute(create_query)

            insert_query = sql.SQL("INSERT INTO {sch_name}.{tbl_name} ({fields}) VALUES ({values})").format(
                sch_name = sql.SQL( schema ),
                tbl_name = sql.SQL( table ),
                fields = sql.SQL( ', ' ).join([sql.SQL("num"), sql.SQL("data")]),
                values = sql.SQL( ', ' ).join([sql.Literal(100), sql.Literal("abc'def")])
                )

            cur.execute(insert_query)

            select_query = sql.SQL("SELECT * FROM {sch_name}.{tbl_name}").format(
                sch_name = sql.SQL( schema ),
                tbl_name = sql.SQL( table ),
            )

            cur.execute(select_query)

            assert cur.fetchone() == (1, 100, "abc'def")

            conn.commit()


def test_drop_table(database, schema="test_schema", table="test"):

    database.drop(schema, table)


def test_datatourisme_schema(datatourisme):

    list_of_columns = ["Nom_du_POI", "Categories_de_POI", "Latitude", "Longitude", "Adresse_postale", "Code_postal_et_commune", "Periodes_regroupees", "Covid19_mesures_specifiques", "Createur_de_la_donnee", "SIT_diffuseur", "Date_de_mise_a_jour", "Contacts_du_POI", "Classements_du_POI", "Description", "URI_ID_du_POI"]

    list_of_columns = [col.lower() for col in list_of_columns]

    assert datatourisme.columns_list() == list_of_columns


def test_create_staging_database(database, datatourisme, schema="test_schema", table_name="test_staging"):
    
    # database.drop(schema, table_name)

    database.create_table(schema, table_name, source=datatourisme)

    database.ingest_from(datatourisme, schema, table_name, region=Region.REUNION)
                

def test_select_one_from_staging(database, schema="test_schema", table_name="test_staging"):

    assert len(database.select_one_from(schema, table_name)) > 0


def test_split_staging(database, datatourisme):
    for type in CATEGORIES.keys():

        schema = "test_" + type

        database.drop_schema_cascade(schema)

        database.create_schema(schema)

        for category in CATEGORIES[type].keys():

            with psycopg.connect(conninfo=database.conn_string) as conn:
                with conn.cursor() as cur:

                    create_query = sql.SQL( "CREATE TABLE IF NOT EXISTS {sch_name}.{tbl_name} ( {fields} );" ).format(
                        sch_name = sql.SQL( schema ),
                        tbl_name = sql.SQL( category ),
                        fields = sql.SQL( ', ' ).join(datatourisme.fields()) )
                    
                    cur.execute(create_query)

                    subcategories = []

                    for subcategory in CATEGORIES[type][category]:
                        
                        subcategories.append( sql.SQL( "{}" ).format( sql.Literal( f"%{subcategory}%" ) ) )

                    
                    insert_query = sql.SQL("""INSERT INTO {sch_name}.{tbl_name} ({fields})
                                                SELECT *
                                                FROM public.test_staging
                                                WHERE public.test_staging.categories_de_poi LIKE ANY(ARRAY[{substrings}]);""").format(
                                                    sch_name = sql.SQL( schema ),
                                                    tbl_name = sql.SQL( category ),
                                                    fields = sql.SQL( ', ' ).join(datatourisme.fields_without_types()),
                                                    substrings = sql.SQL(',').join(subcategories) )

                    print(insert_query)

                    cur.execute(insert_query)

                    conn.commit()

