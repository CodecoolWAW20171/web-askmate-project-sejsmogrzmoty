import db_connection
import psycopg2.sql as sql


COMPARISON_TYPES = ('=', '<>', '<', '>', '<=', '>=', 'LIKE', 'NOT LIKE', 'IN', 'NOT IN')
COMPARISON_TYPES_EXTENDED = ('BETWEEN', 'NOT BETWEEN')
JOIN_WORDS = ('AND', 'OR')
SQL_FUNCTIONS = ('COUNT', 'SUM', 'AVG', '')
ORDER_TYPES = ('ASC', 'DESC')
JOIN_TYPES = ('LEFT', 'RIGHT', 'FULL', '')


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
        if len(column) == 3:
            column = query_column_function(*column)
        elif len(column) == 2:
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
def evaluate_query_WHERE(where):
    if isinstance(where, tuple):
        return construct_query_WHERE(where)
    elif isinstance(where, list):
        return construct_complex_query_WHERE(*where)
    else:
        raise TypeError("Invalid type for WHERE statement.")


def construct_query_WHERE(where):
    where_query, where_values = query_conditional(*where)
    where_query = sql.SQL("WHERE ") + where_query
    return where_query, where_values


def construct_complex_query_WHERE(where_conditionals, where_join_words=[]):
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
            col=query_column(column),
            comp=sql.SQL(comparison),
            vals=sql.SQL(', ').join(sql.Placeholder()*len(values)))

    elif comparison in COMPARISON_TYPES_EXTENDED:
        if len(values) == 2:
            query = sql.SQL("({col} {comp} {val1} AND {val2})").format(
                col=query_column(column),
                comp=sql.SQL(comparison),
                val1=sql.Placeholder(),
                val2=sql.Placeholder())
        else:
            raise ValueError("Exactly 2 values required for BETWEEN conditional.")
    else:
        raise ValueError("Unsupported WHERE conditional.\n    "
                         "(\"{}\" is not a valid comparison type.)".format(comparison))

    return query, values
# ########################################################################


# SQL ORDER BY query construction
# ########################################################################
def construct_query_ORDER_BY(orders):
    """
    Example of usage:
        construct_query_order_by([('answers_number', 'DESC'),
                                 (('question', 'id'), 'ASC')]
    Example of result string representation:
        ORDER BY "answers_number" DESC, "question"."id" ASC

    Args:
        orders (list/tuple): list/tuple of 2-elem list/tuples of strings in form of
            (column to order by, order_type) where order_type is "ASC" or "DESC"

    Returns:
        (psycopg2.sql.Composable) object with an SQL ORDER BY query

    Raises:
        ValueError: if order_type is not "ASC" or "DESC" or if order elements are not
            2-elem lists/tuples
    """

    sql_orders = []
    for order in orders:
        if isinstance(order, (list, tuple)) and len(order) == 2:
            if order[1] in ORDER_TYPES:
                sql_orders.append(sql.SQL(' ').join((query_column(order[0]), sql.SQL(order[1]))))
            else:
                raise ValueError("Invalid order type.")
        else:
            raise ValueError("Invalid syntax. Provide 2-elem list/tuple")

    final_query = sql.SQL("ORDER BY ")+sql.SQL(', ').join(sql_orders)

    return final_query
# ########################################################################


# SQL GROUP BY query construction
# ########################################################################
def construct_query_GROUP_BY(groups):
    sql_groups = [query_column(group) for group in groups]
    final_query = sql.SQL("GROUP BY ")+sql.SQL(', ').join(sql_groups)

    return final_query
# ########################################################################


# SQL JOIN query construction
# ########################################################################
def evaluate_query_JOIN(join_params):
    return construct_query_JOIN(*join_params)


def construct_query_JOIN(table, on_cols, join_type=''):
    join_type = join_type.upper()
    if join_type not in JOIN_TYPES:
        raise ValueError("Unsupported JOIN statement.")
    if len(on_cols) != 2:
        raise ValueError("Exactly 2 columns to join on are required.")
    final_query = sql.SQL("{join_type} JOIN {tbl} ON ({col1}={col2})").format(
        join_type=sql.SQL(join_type),
        tbl=sql.Identifier(table),
        col1=query_column(on_cols[0]),
        col2=query_column(on_cols[1]))

    return final_query
# ########################################################################


# SQL LIMIT query construction
# ########################################################################
def construct_query_LIMIT(limit):
    if isinstance(limit, int):
        final_query = sql.SQL('LIMIT {}').format(sql.Literal(limit))
    else:
        raise ValueError("Limit should be an integer.")

    return final_query
# ########################################################################


# Evaluate optional queries
# ########################################################################
def evaluate_optionals(func, arg):
    if arg is not None:
        return func(arg)
    else:
        if func == evaluate_query_WHERE:
            return (sql.SQL(''), None)
        else:
            return sql.SQL('')
# ########################################################################


# SQL SELECT query
# ########################################################################
@db_connection.connection_handler
def select_query(cursor, table, columns,
                 where=None, orders=None, join_params=None, groups=None, limit=None):

    where_query, where_values = evaluate_optionals(evaluate_query_WHERE, where)
    order_query = evaluate_optionals(construct_query_ORDER_BY, orders)
    join_query = evaluate_optionals(evaluate_query_JOIN, join_params)
    group_query = evaluate_optionals(construct_query_GROUP_BY, groups)
    limit_query = evaluate_optionals(construct_query_LIMIT, limit)

    query = sql.SQL("SELECT {cols} FROM {tbl} {join} {where} {group} {order} {limit};").format(
        cols=choose_columns(columns),
        tbl=sql.Identifier(table),
        join=join_query,
        where=where_query,
        group=group_query,
        order=order_query,
        limit=limit_query
    )

    if where_values:
        cursor.execute(query, where_values)
    else:
        cursor.execute(query)
    data = cursor.fetchall()
    return data
# ########################################################################


# SQL UPDATE query
# ########################################################################
@db_connection.connection_handler
def update_query(cursor, table, columns, values, where=None):

    where_query, where_values = evaluate_optionals(evaluate_query_WHERE, where)

    update_query = sql.SQL("UPDATE {tbl} SET {col_vals} {where}").format(
        tbl=sql.Identifier(table),
        col_vals=sql.SQL(', ').join(sql.SQL("{}={}").format(
            sql.Identifier(column),  sql.Placeholder()) for column in columns),
        where=where_query)

    if where_values is not None:
        values = (*values, *where_values)
    cursor.execute(update_query, values)


@db_connection.connection_handler
def update_increment_query(cursor, table, column, value, where=None):

    where_query, where_values = evaluate_optionals(evaluate_query_WHERE, where)

    update_query = sql.SQL("UPDATE {tbl} SET {col}={col}+({val}) {where}").format(
        tbl=sql.Identifier(table),
        col=sql.Identifier(column),
        val=sql.Placeholder(),
        where=where_query)

    if where_values is not None:
        values = (value, *where_values)
    cursor.execute(update_query, values)
# ########################################################################


# SQL INSERT query
# ########################################################################
@db_connection.connection_handler
def insert_into_query(cursor, table, columns, values):
    insert_query = sql.SQL("INSERT INTO {tbl} ({cols}) VALUES ({val})").format(
        tbl=sql.Identifier(table),
        cols=choose_columns(columns),
        val=sql.SQL(', ').join(sql.Placeholder()*len(values)))
    cursor.execute(insert_query, values)
# ########################################################################


# SQL DELETE query
# ########################################################################
@db_connection.connection_handler
def delete_query(cursor, table, where=None):

    where_query, where_values = evaluate_optionals(evaluate_query_WHERE, where)

    query = sql.SQL("DELETE FROM {tbl} {where}").format(
        tbl=sql.Identifier(table),
        where=where_query)

    if where_values:
        cursor.execute(query, where_values)
    else:
        cursor.execute(query)
# ########################################################################


# Other queries
# ########################################################################
@db_connection.connection_handler
def search_questions(cursor, search_phrase):
    search_string = '%'+search_phrase+'%'
    query = sql.SQL("""
                    SELECT DISTINCT question.*, COUNT(answer.id) as answers_number
                    FROM question LEFT JOIN answer
                    ON question.id=question_id
                    WHERE question.message ILIKE {x}
                    OR question.title ILIKE {x}
                    OR answer.message ILIKE {x}
                    GROUP BY question.id
                    ORDER BY question.submission_time DESC""").format(x=sql.Placeholder())
    cursor.execute(query, (search_string,)*3)
    data = cursor.fetchall()
    return data

@db_connection.connection_handler
def get_all_mates(cursor):

    query ="""
    SELECT username, registration_time , profile_pic, reputation, id
    FROM mate
    ORDER BY username
    """

    cursor.execute(query,)
    data = cursor.fetchall()
    return data