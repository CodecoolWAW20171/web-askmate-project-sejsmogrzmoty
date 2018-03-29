import persistence
import util


# ----- Table names --------------
QSTN_TABLE = 'question'
ANSW_TABLE = 'answer'
CMNT_TABLE = 'comment'
TAG_TABLE = 'tag'
QSTN_TAG_TABLE = 'question_tag'

# ----- Column names -------------
QSTN_HEADERS = ("id", "submission_time", "view_number", "vote_number", "title", "message", "image")
ANSW_HEADERS = ("id", "submission_time", "vote_number", "question_id", "message", "image")
CMNT_HEADERS = ("id", "question_id", "answer_id", "message", "submission_time", "edited_count")

# ----- Column name variables ----
QSTN_ID, QSTN_STIME, QSTN_VIEWN, QSTN_VOTEN, QSTN_TITLE, QSTN_MSG, QSTN_IMG = QSTN_HEADERS
ANSW_ID, ANSW_STIME, ANSW_VOTEN, ANSW_QSTN_ID, ANSW_MSG, ANSW_IMG = ANSW_HEADERS
CMNT_ID, CMNT_QSTN_ID, CMNT_ANSW_ID, CMNT_MSG, CMNT_STIME, CMNT_EDIT_COUNT = CMNT_HEADERS

# ----- Default values -----------
QSTN_DEFAULTS = {"title": "", "message": "", "image": ""}
ANSW_DEFAULTS = {"message": "", "image": ""}
CMNT_DEFAULTS = {"message": ""}

# ----- Constants ----------------
ASC = 'ASC'
DESC = 'DESC'


# Get functions
# ########################################################################
def get_all_questions(limit=None, order_by=None):
    cols = [(QSTN_TABLE, header) for header in QSTN_HEADERS]
    cols.append(('COUNT', (ANSW_TABLE, ANSW_QSTN_ID), 'answers_number'))
    join_on_cols = [(QSTN_TABLE, QSTN_ID), ANSW_QSTN_ID]
    group_by = [(QSTN_TABLE, QSTN_ID)]
    if order_by is None:
        order_by = [(QSTN_STIME, DESC)]
    questions = persistence.select_query(
        table=QSTN_TABLE,
        columns=cols,
        join_params=(ANSW_TABLE, join_on_cols, 'LEFT'),
        groups=group_by,
        orders=order_by,
        limit=limit
    )
    util.convert_time_to_string(questions, QSTN_STIME)
    util.switch_null_to_default(questions, QSTN_DEFAULTS)
    return questions


def get_question(qstn_id):
    questions = get_all_questions()
    for i in questions:
        if i['id'] == qstn_id:
            question = questions[questions.index(i)]
            return question

def get_answer(answ_id):
    answer = persistence.select_query(
        ANSW_TABLE, '*',
        where=(ANSW_ID, '=', (answ_id,)))
    util.convert_time_to_string(answer, ANSW_STIME)
    util.switch_null_to_default(answer, ANSW_DEFAULTS)
    if answer:
        return answer[0]
    return None


def get_answers_to_question(qstn_id):
    answers = persistence.select_query(
        ANSW_TABLE, '*',
        where=(ANSW_QSTN_ID, '=', (qstn_id,)),
        orders=[(ANSW_STIME, DESC)]
    )
    util.convert_time_to_string(answers, ANSW_STIME)
    util.switch_null_to_default(answers, ANSW_DEFAULTS)
    return answers


def get_comment(cmnt_id):
    comment = persistence.select_query(
        CMNT_TABLE, '*',
        where=(CMNT_ID, '=', (cmnt_id,)))
    util.convert_time_to_string(comment, CMNT_STIME)
    util.switch_null_to_default(comment, CMNT_DEFAULTS, (CMNT_ANSW_ID, CMNT_QSTN_ID))
    if comment:
        return comment[0]
    return None


def get_comments_to_question_and_answers(qstn_id, answ_ids):
    if answ_ids:
        where = [
                 [(CMNT_QSTN_ID, '=', (qstn_id,)),
                  (CMNT_ANSW_ID, 'IN', answ_ids)],
                 ["OR"]
                ]
    else:
        where = (CMNT_QSTN_ID, '=', (qstn_id,))

    comments = persistence.select_query(
        CMNT_TABLE, '*',
        where=where,
        orders=[(CMNT_STIME, DESC)])
    util.convert_time_to_string(comments, CMNT_STIME)
    util.switch_null_to_default(comments, CMNT_DEFAULTS, (CMNT_ANSW_ID, CMNT_QSTN_ID))
    return comments


# Add functions
# ########################################################################
def add_new(table, new_input, s_time_name):
    new = {key: (value if value else None) for key, value in new_input.items()}
    new[s_time_name] = util.get_current_time()
    persistence.insert_into_query(
        table=table,
        columns=tuple(new.keys()),
        values=tuple(new.values()))


def add_new_question(new_input):
    add_new(QSTN_TABLE, new_input, QSTN_STIME)


def add_new_answer(new_input):
    add_new(ANSW_TABLE, new_input, ANSW_STIME)


def add_new_comment(new_input):
    add_new(CMNT_TABLE, new_input, CMNT_STIME)


# Modify database
# ########################################################################
def modify(table, id_col_name, id_, modified_input):
    modified = {key: (value if value else None) for key, value in modified_input.items()}
    persistence.update_query(
        table=table,
        columns=modified.keys(),
        values=modified.values(),
        where=(id_col_name, '=', (id_,)))


def modify_question(qstn_id, modified_question):
    modify(QSTN_TABLE, QSTN_ID, qstn_id, modified_question)


def modify_answer(answ_id, modified_answer):
    modify(ANSW_TABLE, ANSW_ID, answ_id, modified_answer)


def modify_comment(cmnt_id, modified_input):
    modified = {key: (value if value else None) for key, value in modified_input.items()}
    modified[CMNT_STIME] = util.get_current_time()
    persistence.update_query(
        table=CMNT_TABLE,
        columns=modified.keys(),
        values=modified.values(),
        where=(CMNT_ID, '=', (cmnt_id,)))
    persistence.update_increment_query(
        table=CMNT_TABLE,
        column=CMNT_EDIT_COUNT,
        value=1,
        where=(CMNT_ID, '=', (cmnt_id,)))


# Delete from database
# ########################################################################
def delete_question(qstn_id):
    persistence.delete_query(QSTN_TABLE, where=(QSTN_ID, '=', (qstn_id,)))


def delete_answer(answ_id):
    persistence.delete_query(ANSW_TABLE, where=(ANSW_ID, '=', (answ_id,)))


def delete_comment(cmnt_id):
    persistence.delete_query(CMNT_TABLE, where=(CMNT_ID, '=', (cmnt_id,)))


# Voting
# ########################################################################
def vote_question(qstn_id, up_or_down):
    persistence.update_increment_query(
        table=QSTN_TABLE,
        column=QSTN_VOTEN,
        value=int(up_or_down),
        where=(QSTN_ID, '=', (qstn_id,)))


def vote_answer(answ_id, up_or_down):
    persistence.update_increment_query(
        table=ANSW_TABLE,
        column=ANSW_VOTEN,
        value=int(up_or_down),
        where=(ANSW_ID, '=', (answ_id,)))


# Views
# ########################################################################
def increase_view_counter(qstn_id):
    persistence.update_increment_query(
        table=QSTN_TABLE,
        column=QSTN_VIEWN,
        value=1,
        where=(QSTN_ID, '=', (qstn_id,)))


# Get top questions
# ########################################################################
def get_most_recent_questions():
    return get_all_questions(5)


def get_most_voted_question():
    return get_all_questions(1, [(QSTN_VOTEN, DESC)])


def get_most_viewed_question():
    return get_all_questions(1, [(QSTN_VIEWN, DESC)])


# Search questions
# ########################################################################
def show_searched_questions(search_phrase):
    questions = persistence.search_questions(search_phrase)
    return questions
