import os
from typing import Dict, List, Tuple

import psycopg2
from psycopg2 import sql


DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')


def get_cursor():
    cursor = conn.cursor()
    return cursor


def fetchall(table: str, columns: List[str]) -> List[Tuple]:
    cursor = get_cursor()
    stmt = sql.SQL('SELECT {} FROM {}').format(
        sql.SQL(',').join(map(sql.Identifier, columns)),
        sql.Identifier(table)
    )
    cursor.execute(stmt)
    rows = cursor.fetchall()
    cursor.close()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def insert(table: str, column_values: Dict):
    cursor = get_cursor()
    columns ='(' + ', '.join( column_values.keys() ) + ')'
    tuple_values = tuple(column_values.values())
    values = "('" + "', '".join(tuple_values) + "')"
    insert = sql.SQL(f"INSERT INTO {table} {columns} VALUES {values}")
    cursor.execute(insert)
    conn.commit()
    cursor.close()