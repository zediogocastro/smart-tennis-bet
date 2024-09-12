from typing import List, Tuple

import psycopg2
from psycopg2.extensions import connection, cursor

from db_values import HOST, USER, PASSWORD, DBNAME
from sql_queries import CREATE_TABLE_QUERIES, DROP_TABLE_QUERIES


def create_database(host: str = HOST,
                    user: str = USER,
                    password: str = PASSWORD,
                    dbname: str = DBNAME
                    ) -> Tuple[cursor, connection]:
    """
    Create fresh "database 'dbname' as user 'user'.

    Parameters
    ----------
    host : str, optional
        Host nanme.
    user : str, optional
        User name.
    password : str, optional
        Password.
    dbname : str, optional
        Database name.

    Returns
    -------
    psycopg2.extensions.cursor, psycopg2.extensions.connection
        Database cursor and connection to 'dbname'.
    """
    DEFAULT_DBNAME = 'postgres'

    # Conect to default database
    conn = psycopg2.connect(host=host, dbname=DEFAULT_DBNAME, user=user, password=password)
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # Create fresh `dbname` database with UTF-8 encoding
    cur.execute(f'DROP DATABASE IF EXISTS {dbname};')
    cur.execute(f'CREATE DATABASE {dbname} WITH ENCODING "UTF8" '
                f'TEMPLATE template0;')

    # Close connection to default database
    conn.close()

    # Connect to the new database
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    return cur, conn

def execute_queries(cur: cursor, queries: List[str]) -> None:
    """
    Execute list of queries in database.

    Parameters
    ----------
    cur : psycopg2.extensions.cursor
        Database cursor.
    queries : list[str]
        List of queries to run.

    Returns
    -------
    None
    """
    for query in queries:
        cur.execute(query)

def main():
    """Main function"""
    cur, conn = create_database()

    execute_queries(cur, queries=DROP_TABLE_QUERIES)
    print('All tables were successfully deleted!')
    execute_queries(cur, queries=CREATE_TABLE_QUERIES)
    print('All tables were successfully created!')

    conn.close()

if __name__ == "__main__":
    main()
    