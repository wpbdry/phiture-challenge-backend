import psycopg2
import psycopg2.extras

import config


def execute_sql(query):
    conn = psycopg2.connect(
        host=config.db_host,
        port=config.db_port,
        dbname=config.db_name,
        user=config.db_user,
        password=config.db_password)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query)
    # The following is copied from
    # https://stackoverflow.com/questions/16519385/output-pyodbc-cursor-results-as-python-dictionary
    columns = [column[0] for column in cur.description]
    function_return = []
    for row in cur.fetchall():
        function_return.append(dict(zip(columns, row)))
    cur.close()
    conn.close()
    return function_return
