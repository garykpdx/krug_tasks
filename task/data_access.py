import psycopg2
from psycopg2 import sql

HOST_NAME = "localhost"
DB_PORT = 5433


class DataAccess:
    def __init__(self):
        self.con = DataAccess.get_connection()
        self.cursor = self.con.cursor()

    @staticmethod
    def get_connection():
        return psycopg2.connect(
            host=HOST_NAME,
            port=DB_PORT,
            database="postgres",
            user="postgres",
            password="ratestask",
        )

    def get_version(self):
        cursor = self.con.cursor()
        cursor.execute('SELECT version() limit 1')
        result, = cursor.fetchone()
        return {'version': result}

    def get_all_subregions(self, region):
        sql = """
            WITH RECURSIVE subregions AS (
            SELECT slug, parent_slug, name
            FROM regions
            WHERE slug=%s
            UNION
                SELECT  r.slug, r.parent_slug, r.name
                FROM regions r
                INNER JOIN subregions sr ON sr.slug = r.parent_slug
        ) SELECT slug FROM subregions;
        """
        cursor = self.con.cursor()
        cursor.execute(sql, (region,))
        return [value[0] for value in cursor.fetchall()]

    def get_ports_from_regions(self, regions):
        cursor = self.con.cursor()
        cursor.execute("SELECT code FROM ports WHERE parent_slug in (%s)", regions)
        return [value[0] for value in cursor.fetchall()]

    def get_prices(self, orig_ports, dest_ports):
        cursor = self.con.cursor()
        cursor.execute("SELECT day, price FROM prices WHERE orig_code in (%s) and dest_code in (%s)",
                       (tuple(orig_ports), tuple(dest_ports)))
        return cursor.fetchall()

    def get_results(self, origin, destination, date_from, date_to):
        cursor = self.con.cursor()
        cursor.execute('SELECT count(*) from ports')
        result, = cursor.fetchone()
        return {'count': result}

    def close(self):
        self.con.close()
