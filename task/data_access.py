from datetime import date

import psycopg2

from task.utils import get_daily_averages

HOST_NAME = "localhost"
DB_PORT = 5433


def is_region(label: str) -> bool:
    return label.islower()


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

    def get_version(self) -> dict:
        cursor = self.con.cursor()
        cursor.execute('SELECT version() limit 1')
        result, = cursor.fetchone()
        return {'version': result}

    def get_all_subregions(self, region: str) -> list:
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

    def get_ports_from_regions(self, regions:list) -> list:
        cursor = self.con.cursor()
        sql_list = "({})".format(','.join(["'%s'" % r for r in regions]))
        sql = "SELECT code FROM ports WHERE parent_slug in %s" % sql_list
        cursor.execute(sql)

        return [value[0] for value in cursor.fetchall()]

    def get_prices(self, orig_ports:list, dest_ports:list, date_from:date, date_to:date) -> list:
        cursor = self.con.cursor()
        orig_ports_list = "({})".format(','.join(["'%s'" % p for p in orig_ports]))
        dest_ports_list = "({})".format(','.join(["'%s'" % p for p in dest_ports]))
        cursor.execute(f"SELECT day, price FROM prices WHERE orig_code in"
                       f" {orig_ports_list} and dest_code in {dest_ports_list} "
                       "and day >= %s and day <= %s", ( date_from, date_to))
        return [(day.strftime('%Y-%m-%d'),price) for day,price in cursor.fetchall()]

    def get_results(self, origin: str, dest: str, date_from: date, date_to: date) -> list:
        origin_list:list = self.get_ports_from_regions(self.get_all_subregions(origin)) if is_region(origin) else [origin]
        dest_list:list = self.get_ports_from_regions(self.get_all_subregions(dest)) if is_region(dest) else [dest]
        prices:list = self.get_prices(origin_list, dest_list, date_from, date_to)
        return get_daily_averages(prices)

    def close(self):
        self.con.close()
