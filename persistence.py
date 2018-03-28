import os
import psycopg2
import psycopg2.extras
import psycopg2.sql as sql


QSTN_TABLE = 'question'
ANSW_TABLE = 'answer'
CMNT_TABLE = 'comment'
TAG_TABLE = 'tag'
QSTN_TAG_TABLE = 'question_tag'
QSTN_VIEW_COLUMNS = ['id', 'submission_time', 'view_number', 'vote_number', 'title']
QSTN_COLUMNS = ['submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
COMPARISON_TYPES = ('=', '<>', '<', '>', 'LIKE', 'NOT LIKE', 'IN', 'NOT IN')
ASC = 'ASC'
DESC = 'DESC'


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


def change_time_to_string(data):
    for index, single_data in enumerate(data):
        data[index][SBMSN_TIME] = str(data[index][SBMSN_TIME])
    return data


def choose_columns(columns):
    if columns == '*':
        columns = sql.SQL('*')
    elif isinstance(columns, (list, tuple)):
        columns = sql.SQL(', ').join(map(sql.Identifier, columns))
    else:
        raise TypeError("Columns to select specified invalidly.")
    return columns


def construct_query_where(where):
    if where is not None:
        where_col, where_comparison, values = where
        if where_comparison.upper() in COMPARISON_TYPES:
            where_comparison = sql.SQL(where_comparison.upper())
        else:
            raise ValueError("Unsupported WHERE conditional.")

        where_query = sql.SQL("WHERE {col} {comp} ({vals})").format(
            col=sql.Identifier(where_col),
            comp=where_comparison,
            vals=sql.SQL(', ').join(sql.Placeholder()*len(values)))
    else:
        where_query = sql.SQL('')
    return where_query


@connection_handler
def select_query(cursor, table, columns, where=None, order_by=None, order_type=None, limit=None):

    where_query = construct_query_where(where)

    if order_by is not None:
        ordered_by = sql.SQL('ORDER BY {}').format(sql.Identifier(order_by))
    else:
        ordered_by = sql.SQL('')

    if order_type is not None:
        type_of_order = sql.SQL(order_type.upper())
    else:
        type_of_order = sql.SQL('')

    if limit is not None:
        limited_to = sql.SQL('LIMIT {}').format(sql.Literal(limit))
    else:
        limited_to = sql.SQL('')

    query = sql.SQL(
        "SELECT {col_data} FROM {table_data} {where_data} {order_by_data} {order_type_data} {limit_data};").format(
        col_data=choose_columns(columns),
        table_data=sql.Identifier(table),
        where_data=where_query,
        order_by_data=ordered_by,
        order_type_data=type_of_order,
        limit_data=limited_to
    )

    if where_query == sql.SQL(''):
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    else:
        cursor.execute(query, where[2])
        data = cursor.fetchall()
        return data


@connection_handler
def update(cursor, table, columns, values, where=None):

    where_query = construct_query_where(where)

    update_query = sql.SQL("UPDATE {tbl} SET {col_vals} {where}").format(
        tbl=sql.Identifier(table),
        col_vals=sql.SQL(', ').join(sql.SQL("{}={}").format(
            sql.Identifier(column),  sql.Placeholder()) for column in columns),
        where=where_query)
    if where is not None:
        values = (*values, *where[2])
    cursor.execute(update_query, values)


@connection_handler
def insert_into(cursor, columns, table, values):
    insert_query = sql.SQL("INSERT INTO {tbl} ({cols}) VALUES ({val})").format(
        tbl=sql.Identifier(table),
        cols=choose_columns(columns),
        val=sql.SQL(",").join(sql.Placeholder()*len(values)))
    cursor.execute(insert_query, values)


def delete_query(table):
    query = sql.SQL("DELETE FROM {tbl} ").format(tbl=sql.Identifier(table))
    return query


@connection_handler
def delete_from_table(cursor, table, where):
    cursor.execute(delete_query(table)+construct_query_where(where), where[2])
