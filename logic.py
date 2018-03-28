import persistence
import util

QSTN_TABLE = 'question'
ANSW_TABLE = 'answer'
CMNT_TABLE = 'comment'
TAG_TABLE = 'tag'
VOTE_CLMN = 'vote_number'
QSTN_TAG_TABLE = 'question_tag'
TABLES = [QSTN_TABLE, ANSW_TABLE, CMNT_TABLE, TAG_TABLE, QSTN_TAG_TABLE]
QSTN_COLUMNS = ['id', 'submission_time', 'view_number', 'vote_number', 'title']
ASC = 'ASC'
DESC = 'DESC'

SBMSN_TIME = 'submission_time'

# ----- Constants -----------
QSTN_HEADERS = ("id", "submission_time", "view_number", "vote_number", "title", "message", "image")
ANSW_HEADERS = ("id", "submission_time", "vote_number", "question_id", "message", "image")
ANSW_DEFAULTS = {"vote_number": 0, "message": "", "image": ""}

# ----- Column indecies -----
QSTN_ID, QSTN_STIME, QSTN_VIEWN, QSTN_VOTEN, QSTN_TITLE, QSTN_MSG, QSTN_IMG = QSTN_HEADERS
ANSW_ID, ANSW_STIME, ANSW_VOTEN, ANSW_QSTN_ID, ANSW_MSG, ANSW_IMG = ANSW_HEADERS

# ----- Default values ------
QSTN_DEFAULTS = {"view_number": 0, "vote_number": 0, "title": "", "message": "", "image": ""}
CMNT_DEFAULTS = {"message": ""}


# Get functions
# ########################################################################
def get_all_questions():
    cols = [(QSTN_TABLE, header) for header in
            (QSTN_ID, QSTN_STIME, QSTN_TITLE, QSTN_VIEWN, QSTN_VOTEN)]
    cols.append(('COUNT', (ANSW_TABLE, ANSW_QSTN_ID), 'answers_number'))
    join_on_cols = [(QSTN_TABLE, QSTN_ID), ANSW_QSTN_ID]
    group_by = [(QSTN_TABLE, QSTN_ID)]
    order_by = [(QSTN_STIME, DESC)]
    questions = persistence.select_query(
        table=QSTN_TABLE,
        columns=cols,
        join=(ANSW_TABLE, join_on_cols, 'LEFT'),
        groups=group_by,
        orders=order_by
    )
    util.convert_time_to_string(questions, QSTN_STIME)
    return questions


def get_question(qstn_id):
    question = persistence.select_query(QSTN_TABLE, '*', wheres=[[('id', '=', (qstn_id,))]])
    util.convert_time_to_string(question, QSTN_STIME)
    return question[0]


def get_answer(answ_id):
    answer = persistence.select_query(ANSW_TABLE, '*', wheres=[[('id', '=', (answ_id,))]])
    util.convert_time_to_string(answer, ANSW_STIME)
    return answer[0]


def get_answers_to_question(qstn_id):
    answers = persistence.select_query(
        ANSW_TABLE, '*',
        wheres=[[(ANSW_QSTN_ID, '=', (qstn_id,))]],
        orders=[(ANSW_STIME, DESC)]
    )
    util.convert_time_to_string(answers, ANSW_STIME)
    return answers


# def get_comments_to_question(qstn_id):
#     comments = persistence.select_query(CMNT_TABLE, '*', ('question_id', '=', (qstn_id,)), 'submission_time', DESC)
#     convert_time_to_string(comments)
#     return comments


# def get_comments_to_answer(answ_id):
#     comments = persistence.select_query(CMNT_TABLE, '*', ('question_id', '=', (answ_id,)), 'submission_time', DESC)
#     convert_time_to_string(comments)
#     return comments


# Add functions
# ########################################################################
def add_new_question(new_question_input):
    new_question = {key: new_question_input[key] for key in new_question_input}
    new_question[QSTN_STIME] = util.get_current_time()
    persistence.insert_into(
        table=QSTN_TABLE,
        columns=tuple(new_question.keys()),
        values=tuple(new_question.values())
    )


def add_new_answer(new_answer_input):
    new_answer = {key: new_answer_input[key] for key in new_answer_input}
    new_answer[ANSW_STIME] = util.get_current_time()
    persistence.insert_into(
        table=ANSW_TABLE,
        columns=tuple(new_answer.keys()),
        values=tuple(new_answer.values())
    )


def add_new_comment(new_comment_input):
    new_comment = {key: new_comment_input[key] for key in new_comment_input}
    new_comment[SBMSN_TIME] = util.get_current_time()
    persistence.insert_into(
        table=CMNT_TABLE,
        columns=tuple(new_comment.keys()),
        values=tuple(new_comment.values())
    )


# Modify question database
# ########################################################################
def modify_question(qstn_id, modified_question):

    persistence.update(table=QSTN_TABLE,
                       columns=modified_question.keys(),
                       values=modified_question.values(),
                       wheres=[[('id', '=', (qstn_id,))]])


def modify_answer(answ_id, modified_answer):

    persistence.update(table=ANSW_TABLE,
                       columns=modified_answer.keys(),
                       values=modified_answer.values(),
                       wheres=[[('id', '=', (answ_id,))]])


def delete_question(qstn_id):
    persistence.delete_query(QSTN_TABLE, wheres=[[('id', '=', (qstn_id,))]])


def delete_answer(answ_id):
    persistence.delete_query(ANSW_TABLE, wheres=[[('id', '=', (answ_id,))]])


def modify_comment_of_answer(answ_id, modified_comment):

    persistence.update(table=CMNT_TABLE,
                       columns=modified_comment.keys(),
                       values=modified_comment.values(),
                       where=('answer_id', '=', (answ_id,)))


def modify_comment_of_question(qstn_id, modified_comment):

    persistence.update(table=CMNT_TABLE,
                       columns=modified_comment.keys(),
                       values=modified_comment.values(),
                       where=('question_id', '=', (qstn_id,)))


def delete_question(qstn_id):
    persistence.delete_from_table(QSTN_TABLE, ('id', '=', (qstn_id,)))


def delete_answer(answ_id):
    persistence.delete_from_table(ANSW_TABLE, ('id', '=', (answ_id)))


def delete_comment_of_question(qstn_id):
    persistence.delete_from_table(CMNT_TABLE, ('question_id', '=', (qstn_id,)))


def delete_comment_of_answer(answ_id):
    persistence.delete_from_table(CMNT_TABLE, ('answer_id', '=', (answ_id,)))


# Voting
# ########################################################################
def vote_question(id_, up_or_down):
    persistence.update_vote_number(
        QSTN_TABLE,
        VOTE_CLMN,
        int(up_or_down),
        ('id', '=', (id_,)))


def vote_answer(id_, up_or_down):
    persistence.update_vote_number(
        ANSW_TABLE,
        VOTE_CLMN,
        int(up_or_down),
        ('id', '=', (id_,)))


# Get top questions
# ########################################################################
def get_most_recent_questions(limit):
    questions = persistence.select_query(
        QSTN_TABLE, QSTN_HEADERS, order_by='submission_time', order_type=DESC, limit=limit)
    util.convert_time_to_string(questions)
    return questions


def get_most_voted_question(limit):
    questions = persistence.select_query(
        QSTN_TABLE, QSTN_HEADERS, order_by='vote_number', order_type=DESC, limit=limit)
    util.convert_time_to_string(questions)
    return questions


def get_most_viewed_question(limit):
    questions = persistence.select_query(QSTN_TABLE, QSTN_HEADERS, order_by='view_number', order_type=DESC, limit=limit)
    util.convert_time_to_string(questions)
    return questions
