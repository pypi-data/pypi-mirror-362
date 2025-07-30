import logging
import os

from geoalchemy2 import Geometry
from psycopg2 import errors, sql
from sqlalchemy import Column, MetaData, Table, create_engine
from sqlalchemy.dialects.postgresql import DATE, NUMERIC, VARCHAR

log = logging.getLogger(__name__)


class Database(object):
    """Wrapper around sqlalchemy"""

    def __init__(self, url=os.environ.get("DATABASE_URL")):
        self.url = url
        self.engine = create_engine(url)
        # make sure postgis is available
        try:
            self.query("SELECT postgis_full_version()")
        except errors.UndefinedFunction:
            log.error(
                "Cannot find PostGIS, has extension been installed on database %s ?",
                url,
            )
            raise errors.UndefinedFunction

        # supported oracle/wfs to postgres types
        self.supported_types = {
            "NUMBER": NUMERIC,
            "VARCHAR2": VARCHAR,
            "DATE": DATE,
        }

    @property
    def schemas(self):
        """List all non-system schemas in db"""
        sql = """SELECT schema_name FROM information_schema.schemata
                 ORDER BY schema_name"""
        schemas = self.query(sql)
        return [s[0] for s in schemas if s[0][:3] != "pg_"]

    @property
    def tables(self):
        """List all non-system tables in the db"""
        tables = []
        for schema in self.schemas:
            tables = tables + [schema + "." + t for t in self.tables_in_schema(schema)]
        return tables

    def tables_in_schema(self, schema):
        """Get a listing of all tables in given schema"""
        sql = """SELECT table_name
                 FROM information_schema.tables
                 WHERE table_schema = %s"""
        return [t[0] for t in self.query(sql, (schema,))]

    def query(self, sql, params=None):
        """Execute sql and return all results"""
        conn = self.engine.raw_connection()
        with conn.cursor() as curs:
            curs.execute(sql, params)
            result = curs.fetchall()
        return result

    def execute(self, sql, params=None):
        """Execute sql and return only whether the query was successful"""
        conn = self.engine.raw_connection()
        with conn.cursor() as curs:
            result = curs.execute(sql, params)
            conn.commit()
        return result

    def execute_many(self, sql, params):
        """Execute many sql"""
        conn = self.engine.raw_connection()
        with conn.cursor() as curs:
            curs.executemany(sql, params)
            conn.commit()

    def create_schema(self, schema):
        if schema not in self.schemas:
            log.info(f"Schema {schema} does not exist, creating it")
            dbq = sql.SQL("CREATE SCHEMA {schema}").format(schema=sql.Identifier(schema))
            self.execute(dbq)

    def drop_table(self, schema, table):
        if schema + "." + table in self.tables:
            log.info(f"Dropping table {schema}.{table}")
            dbq = sql.SQL("DROP TABLE {schema}.{table}").format(
                schema=sql.Identifier(schema),
                table=sql.Identifier(table),
            )
            self.execute(dbq)

    def refresh(self, schema, table):
        # move data from temp table to target table
        if schema + "." + table in self.tables:
            log.warning(f"Truncating table {schema}.{table} and refreshing from bcdata.{table}")
            dbq = sql.SQL("TRUNCATE {schema}.{table}").format(
                schema=sql.Identifier(schema),
                table=sql.Identifier(table),
            )
            self.execute(dbq)
            columns = list(
                set(self.get_columns("bcdata", table)).intersection(self.get_columns(schema, table))
            )
            identifiers = [sql.Identifier(c) for c in columns]
            dbq = sql.SQL(
                """INSERT INTO {schema}.{table}
                ({columns})
                SELECT {columns} FROM bcdata.{table}"""
            ).format(
                schema=sql.Identifier(schema),
                table=sql.Identifier(table),
                columns=sql.SQL(",").join(identifiers),
            )
            self.execute(dbq)
            self.drop_table("bcdata", table)
        else:
            raise ValueError(f"Target table {schema}.{table} does not exist in database")

    def define_table(
        self,
        schema_name,
        table_name,
        table_details,
        geom_type,
        promote_to_multi=True,
        table_comments=None,
        primary_key=None,
    ):
        """build sqlalchemy table definition from bcdc provided json definitions"""
        # remove columns of unsupported types, redundant columns
        table_details = [c for c in table_details if c["data_type"] in self.supported_types.keys()]
        table_details = [
            c
            for c in table_details
            if c["column_name"] not in ["FEATURE_AREA_SQM", "FEATURE_LENGTH_M"]
        ]

        # translate the oracle types to sqlalchemy provided postgres types
        columns = []
        for i in range(len(table_details)):
            column_name = table_details[i]["column_name"].lower()
            column_type = self.supported_types[table_details[i]["data_type"]]
            # append precision if varchar or numeric
            if table_details[i]["data_type"] == "VARCHAR2":
                column_type = column_type(int(table_details[i]["data_precision"]))
            # check that comments are present
            if "column_comments" in table_details[i].keys():
                column_comments = table_details[i]["column_comments"]
            else:
                column_comments = None
            if column_name == primary_key:
                columns.append(
                    Column(
                        column_name,
                        column_type,
                        primary_key=True,
                        comment=column_comments,
                    )
                )
            else:
                columns.append(
                    Column(
                        column_name,
                        column_type,
                        comment=column_comments,
                    )
                )

        # make everything multipart
        # (some datasets have mixed singlepart/multipart geometries)
        if promote_to_multi and geom_type[:5] != "MULTI":
            geom_type = "MULTI" + geom_type
        columns.append(Column("geom", Geometry(geom_type, srid=3005)))
        metadata_obj = MetaData()
        table = Table(
            table_name,
            metadata_obj,
            *columns,
            comment=table_comments,
            schema=schema_name,
        )

        if schema_name not in self.schemas:
            self.create_schema(schema_name)

        # drop existing table
        if schema_name + "." + table_name in self.tables:
            log.warning(f"Table {schema_name}.{table_name} exists, overwriting")
            self.drop_table(schema_name, table_name)

        # create the table
        if schema_name + "." + table_name not in self.tables:
            log.info(f"Creating table {schema_name}.{table_name}")
            table.create(self.engine)

        return table

    def get_columns(self, schema, table):
        metadata_obj = MetaData(schema=schema)
        table = Table(table, metadata_obj, schema=schema, autoload_with=self.engine)
        return list(table.columns.keys())

    def log(self, schema_name, table_name):
        log.info("Logging download date to bcdata.log")
        self.execute(
            """CREATE SCHEMA IF NOT EXISTS bcdata;
               CREATE TABLE IF NOT EXISTS bcdata.log (
                 table_name text PRIMARY KEY,
                 latest_download timestamp WITH TIME ZONE
               );
            """
        )
        self.execute(
            """INSERT INTO bcdata.log (table_name, latest_download)
               SELECT %s as table_name, NOW() as latest_download
               ON CONFLICT (table_name) DO UPDATE SET latest_download = NOW();
            """,
            (schema_name + "." + table_name,),
        )
