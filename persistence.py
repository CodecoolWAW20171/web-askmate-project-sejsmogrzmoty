import db_connection
import psycopg2.sql as sql


QSTN_TABLE = 'question'
ANSW_TABLE = 'answer'
CMNT_TABLE = 'comment'
TAG_TABLE = 'tag'
QSTN_TAG_TABLE = 'question_tag'
QSTN_VIEW_COLUMNS = ['id', 'submission_time', 'view_number', 'vote_number', 'title']
QSTN_COLUMNS = ['submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']

COMPARISON_TYPES = ('=', '<>', '<', '>', '<=', '>=', 'LIKE', 'NOT LIKE', 'IN', 'NOT IN')
COMPARISON_TYPES_EXTENDED = ('BETWEEN', 'NOT BETWEEN')
JOIN_WORDS = ('AND', 'OR')
SQL_FUNCTIONS = ('COUNT', 'SUM', 'AVG', '')

ASC = 'ASC'
DESC = 'DESC'


# SQL column query construction
# ########################################################################
def choose_columns(columns):
    """
    Create a part of SQL query with column names.
    Example of return string representation:
        "id", "first_name", "last_name", "column4"

    Args:
        columns (list/tuple): a list/tuple of strings with column names
            or a string '*' which is equavialent to SQL * i.e. all columns

    Returns:
        (psycopg2.sql.SQL) object with a list of comma separated column names.

    Raises:
        TypeError: if argument columns is not an instance of list/tuple
            or a string '*'
    """

    if columns == '*':
        columns = sql.SQL('*')
    elif isinstance(columns, (list, tuple)):
        sql_columns = []
        for column in columns:
            sql_columns.append(query_column(column))
        columns = sql.SQL(', ').join(sql_columns)
    else:
        raise TypeError("Invalid syntax. Specify either list/tuple of columns or \"*\"")

    return columns


def query_column(column):
    """
    Example of string representation of return value:
        query_column('id') -> "id"
        query_column(('question', '*')) -> "question".*
        query_column(('COUNT', 'id', 'number')) -> COUNT("id") AS "number"

    Args:
        column (string/list/tuple): string with column name or list/tuple of strings
            with column parameters:
                string -> only column name
                2 elem list/tuple -> table name and column name respectively
                3 elem list/tuple -> see query_column_function

    Returns:
        (psycopg2.sql.Composable) object with an SQL column query
    """

    if isinstance(column, (list, tuple)):
        if len(column) > 2:
            column = query_column_function(*column)
        elif len(column) > 1:
            if column[1] == '*':
                column = (sql.Identifier(column[0]), sql.SQL('*'))
            else:
                column = map(sql.Identifier, column)
            column = sql.SQL('.').join(column)
        else:
            column = sql.Identifier(column[0])
    else:
        column = sql.Identifier(column)

    return column


def query_column_function(function, column, alias):
    """
    Example of string representation of return value:
        query_column_function('COUNT', 'id', 'number') -> COUNT("id") AS "number"

    Returns:
        (psycopg2.sql.Composable) object with an SQL column function query
    """

    function = function.upper()
    if function in SQL_FUNCTIONS:
        query = sql.SQL("{func}({col}) AS {alias}").format(
            func=sql.SQL(function),
            col=query_column(column),
            alias=sql.Identifier(alias))
    else:
        raise ValueError("Unsupported function.")

    return query
# ########################################################################


# SQL WHERE query construction
# ########################################################################
def construct_query_where(where_conditionals, where_join_words=[]):
    """
    Construct a complex WHERE query. Example:
        construct_query_where(
            [('view_number', '>', (50,)),
             ('title', 'LIKE', ('How do I%',)),
             ('vote_number', 'BETWEEN', (0, 10))],
            ["AND", "OR"]
        )

    Args:
        where_conditionals (list): list of 3-element tuples with WHERE conditions,
            i.e. (column, comparison_type, values)
        where_join_words (list): list of strings with join words for conditional
            statements (either "AND" or "OR")

    Returns:
        (tuple) with psycopg2.sql.SQL object as query and a list values for placeholders
            i.e. (psycopg2.sql.SQL query, list of values)
    Raises:
        ValueError: if incorrect input is detected (multiple checks)
    """

    if len(where_conditionals)-1 != len(where_join_words):
        raise ValueError("Incorrect number of condition join words.\n    "
                         "For {} WHERE conditionals expected {} join words.".format(
                             len(where_conditionals), len(where_conditionals)-1
                         ))

    # get list of tuples in form (SQL query for condition, values for placeholder)
    QRY, VAL = 0, 1
    queries = []
    for where in where_conditionals:
        if len(where) == 3:
            queries.append(query_conditional(*where))
        else:
            raise ValueError("3 arguments expected for WHERE conditional (column, comparison, values)")

    # join queries with conditions into one WHERE query using given join types
    final_query = sql.SQL("WHERE ") + queries[0][QRY]
    values = [*queries[0][VAL]]
    for w, join_word in enumerate(where_join_words, 1):
        join_word = join_word.upper()
        if join_word in JOIN_WORDS:
            final_query = sql.SQL(' ').join([final_query, sql.SQL(join_word), queries[w][QRY]])
        else:
            raise ValueError("Unsupported WHERE conditional join word. (Only \"AND\" or \"OR\" allowed.)")
        values.extend(queries[w][VAL])

    return final_query, values


def query_conditional(column, comparison, values):
    """

    """

    comparison = comparison.upper()

    if comparison in COMPARISON_TYPES:
        query = sql.SQL("({col} {comp} ({vals}))").format(
            col=sql.Identifier(column),
            comp=sql.SQL(comparison),
            vals=sql.SQL(', ').join(sql.Placeholder()*len(values)))

    elif comparison in COMPARISON_TYPES_EXTENDED:
        if len(values) == 2:
            query = sql.SQL("({col} {comp} {val1} AND {val2})").format(
                col=sql.Identifier(column),
                comp=sql.SQL(comparison),
                val1=sql.Placeholder(),
                val2=sql.Placeholder())
        else:
            raise ValueError("Exactly 2 values required for BETWEEN conditional.")
    else:
        raise ValueError("Unsupported WHERE conditional.\n    "
                         "(\"{}\" is not a valid comparison type.)".format(comparison)
                        )

    return query, values
# ########################################################################


# SQL ORDER BY query construction
# ########################################################################
def construct_query_order_by(orders):
    for order in orders:
        if isinstance(order, (list, tuple)) and len(order) == 2:
            if order[1] in ORDER


import datetime
@db_connection.connection_handler
def test(cursor):
    # wheres = [
    #     ('view_number', '>=', (0,)),
    #     ('submission_time', 'between', (datetime.datetime(2017,4,29), datetime.datetime.now()))
    # ]
    # long_q = construct_query_where(wheres, ['and'])
    # print(long_q[0].as_string(cursor))
    # print(long_q[1])
    cols = (('question', 'id'),
            ('question', 'submission_time'),
            ('question', 'view_number'),
            ('question', 'vote_number'),
            ('COUNT', ('answer', 'id'), 'answers_number'))
    q_final = sql.SQL("SELECT {cols} FROM {tbl} JOIN answer ON (question.id=question_id) GROUP BY question.id {where}").format(
        tbl=sql.Identifier('question'),
        cols=choose_columns(cols),
        where=sql.SQL(''))
    print(q_final.as_string(cursor))
    cursor.execute(q_final)
    data = cursor.fetchall()
    print(data)
    return data

import ui
ui.print_table(test())




# ########################################################################
@db_connection.connection_handler
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


@db_connection.connection_handler
def update(cursor, table, columns, values, where=''):

    where = construct_query_where(where)

    update_query = sql.SQL("UPDATE {tbl} SET {col_vals} {where}").format(
        tbl=sql.Identifier(table),
        col_vals=sql.SQL(', ').join(sql.SQL("{}={}").format(
            sql.Identifier(column),  sql.Placeholder()) for column in columns),
        where=where_query)
    if where is not None:
        values = (*values, *where[2])
    cursor.execute(update_query, values)


@db_connection.connection_handler
def insert_into(cursor, columns, table, values):
    insert_query = sql.SQL("INSERT INTO {tbl} ({cols}) VALUES ({val})").format(
        tbl=sql.Identifier(table),
        cols=choose_columns(columns),
        val=sql.SQL(",").join(sql.Placeholder()*len(values)))
    cursor.execute(insert_query, values)


def delete_query(table):
    query = sql.SQL("DELETE FROM {tbl} ").format(tbl=sql.Identifier(table))
    return query


@db_connection.connection_handler
def delete_from_table(cursor, table, where):
    cursor.execute(delete_query(table)+construct_query_where(where), where[2])


@connection_handler
def show_all_questions_with_counter(cursor):
    cursor.execute("""
                    SELECT question.*, COUNT(answer.id) as answers_number
                    FROM question
                    JOIN answer ON question.id=question_id
                    GROUP BY question.id;
                    """)
    data = cursor.fetchall()
    return data


@connection_handler
def get_comments_for_answers_and_questions(cursor, answers_ids, qstn_id):
    query = sql.SQL('SELECT * FROM comment WHERE {} IN ({}) OR {}={}').format(
        sql.Identifier('answer_id'),
        sql.Placeholder()*len(answers_ids),
        sql.Identifier('question_id'),
        sql.Literal(qstn_id)
    )
    cursor.execute(query, answers_ids)
    data = cursor.fetchall()
    return data
