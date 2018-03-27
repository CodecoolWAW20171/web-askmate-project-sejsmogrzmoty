import os
import psycopg2
import psycopg2.extras
import psycopg2.sql as sql


def get_connection_string():
    # setup connection string
    # to do this, please define these environment variables first
    user_name = os.environ.get('PSQL_USER_NAME')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    database_name = os.environ.get('PSQL_DB_NAME')

    env_variables_defined = user_name and password and host and database_name

    if env_variables_defined:
        # this string describes all info for psycopg2 to connect to the database
        return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
            user_name=user_name,
            password=password,
            host=host,
            database_name=database_name
        )
    else:
        raise KeyError('Some necessary environment variable(s) are not defined')


def open_database():
    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a RealDictCursor cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value
    return wrapper


@connection_handler
def select_all_from_table(cursor, table):
    cursor.execute(sql.SQL('SELECT * FROM {}').format(sql.Identifier(table)))
    data = cursor.fetchall()
    return data


@connection_handler
def select_columns_from_table(cursor, table, select_cols):
    if select_cols == '*':
        select_cols = sql.SQL('*')
    elif isinstance(select_cols, (list, tuple)):
        select_cols = sql.SQL(', ').join(map(sql.Identifier, select_cols))
    else:
        raise TypeError("Columns to select specified invalidly.")

    query = sql.SQL("SELECT {cols} FROM {tbl};").format(
        cols=select_cols,
        tbl=sql.Identifier(table))
    cursor.execute(query)
    data = cursor.fetchall()
    return data


@connection_handler
def select_where(cursor, table, select_cols,
                 where_col, where_comparison, values):

    if where_comparison.upper() in ('=', '<>', 'LIKE', 'NOT LIKE', 'IN', 'NOT IN'):
        where_comparison = sql.SQL(where_comparison.upper())
    else:
        raise ValueError("Unsupported WHERE conditional.")

    if select_cols == '*':
        select_cols = sql.SQL('*')
    elif isinstance(select_cols, (list, tuple)):
        select_cols = sql.SQL(', ').join(map(sql.Identifier, select_cols))
    else:
        raise TypeError("Columns to select specified invalidly.")

    query = sql.SQL("SELECT {cols} FROM {tbl} WHERE {col} {comp} ({vals});").format(
        cols=select_cols,
        tbl=sql.Identifier(table),
        col=sql.Identifier(where_col),
        comp=where_comparison,
        vals=sql.SQL(', ').join(sql.Placeholder()*len(values)))

    print(query.as_string(cursor))
    cursor.execute(query, values)
    data = cursor.fetchall()
    return data


def select_all_from_table(cursor, table, order_by):
    cursor.execute(
        sql.SQL('SELECT * FROM {} ORDER BY {}').format(
            sql.Identifier(table), sql.Identifier(order_by)
        )
    )
    return cursor.fetchall()


@connection_handler
def select_specific_from_table(cursor, columns, table):
    cursor.execute(
        sql.SQL('SELECT {} FROM {}').format(
            sql.SQL(', ').join(sql.Identifier(column) for column in columns), (sql.Identifier(table))))
    return cursor.fetchall()


# @connection_handler
# def select_specific_from_table(cursor, table, id):
