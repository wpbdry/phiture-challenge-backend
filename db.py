import psycopg2

import config


def connect():
    return psycopg2.connect(
        host=config.db_host,
        port=config.db_port,
        dbname=config.db_name,
        user=config.db_user,
        password=config.db_password)

def execute_sql(query):
    conn = connect()
    cur = conn.cursor()
    cur.execute(query)
    function_return = cur.fetchall()
    cur.close()
    return function_return
