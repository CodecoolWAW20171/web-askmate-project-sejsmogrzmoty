

# Note: no safeguard against wide columns - terminals wrap long lines.
# If use suspect wide column be sure to stretch terminal beforehand or
# run fullscreen
def print_table(table, headers={}, head_form=['<'], cell_form=['<']):
    """
    Prints table with data.

    Args:
        table (list): list of dictionaries to display
        headers (dict): dict or better OrderedDict containing keys to table
            dictionaries and corresponding table headers
        head_form (list): list with headers formatting for str.format funciton
        celll_form (list): list with column cells formatting for str.format
            funciton

    Returns:
        This function doesn't return anything it only prints to console.
    """

    # formats
    sep_s = '|'
    mid_sep = ' '+sep_s+' '
    left_sep = sep_s+' '
    right_sep = ' '+sep_s
    seps = (left_sep, mid_sep, right_sep)

    # handle empty table
    if len(table) < 1:
        if headers:
            table = [{key: '' for key in headers}]
        else:
            return False

    headers = {key: (key if key not in headers else headers[key]) for key in table[0]}

    # fill with default values if empty
    n_cols = len(headers)
    n_rows = len(table)
    head_form = fill_empty(head_form, n_cols, head_form[0])
    cell_form = fill_empty(cell_form, n_cols, cell_form[0])

    # column widths
    coll_widths = [max(str_len(row[key]) for row in table) for key in headers]
    # final widths considering headers width
    widths = [max(str_len(header), coll_widths[c]) for c, header in enumerate(headers.values())]
    total_width = sum(widths) + len(left_sep) + len(mid_sep)*(n_cols-1) + len(right_sep)

    # formatting
    h_form = [head_form[w]+str(width) for w, width in enumerate(widths)]
    c_form = [cell_form[w]+str(width) for w, width in enumerate(widths)]

    # line separator
    line_seperator = ['-'*(w+2) for w in widths]
    line_seperator.insert(0, '')
    line_seperator.append('')
    line_seperator = sep_s.join(line_seperator)

    # actual printing
    print('/', '-'*(total_width-2), '\\', sep='')
    if any(headers.values()):
        print_row(headers, headers, n_cols, h_form, seps)
        print('\n'+line_seperator)

    for r, row in enumerate(table):
        print_row(row, headers, n_cols, c_form, seps)
        if r < n_rows-1:
            print()
    print()
    print('\\', '-'*(total_width-2), '/', sep='')


def print_row(row, cols, n_cols, form, seps):
    print(seps[0], end='')
    for c, col in enumerate(cols):
        print("{:{}}".format(str(row[col]), form[c]), end='')
        if c < n_cols-1:
            print(seps[1], end='')
        else:
            print(seps[2], end='')


def str_len(string_):
    return len(str(string_))


def fill_empty(list_, length, default):
    n = length - len(list_)
    for _ in range(n):
        list_.append(default)
    return list_
