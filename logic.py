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
COMPARISON_TYPES = ('=', '<>', '<', '>', 'LIKE', 'NOT LIKE', 'IN', 'NOT IN')
ASC = 'ASC'
DESC = 'DESC'

SBMSN_TIME = 'submission_time'

# ----- Constants -----------
QSTN_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSW_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
ANSW_DEFAULTS = {"vote_number": 0, "message": "", "image": ""}

# ----- Column indecies -----
QSTN_ID, QSTN_STIME, QSTN_VIEWN, QSTN_VOTEN, QSTN_TITLE, QSTN_MSG, QSTN_IMG = range(len(QSTN_HEADERS))
ANSW_ID, ANSW_STIME, ANSW_VOTEN, ANSW_QSTN_ID, ANSW_MSG, ANSW_IMG = range(len(ANSW_HEADERS))

# ----- Default values ------
QSTN_DEFAULTS = {"view_number": 0, "vote_number": 0, "title": "", "message": "", "image": ""}
CMNT_DEFAULTS = {"message": ""}

# Get functions
# ########################################################################


def convert_time_to_string(data):
    for index, single_data in enumerate(data):
        data[index][SBMSN_TIME] = str(data[index][SBMSN_TIME])
    return data


def get_all_questions():
    questions = persistence.select_query(
        table=QSTN_TABLE,
        columns=(QSTN_HEADERS)
    )
    convert_time_to_string(questions)
    return questions


def get_question(qstn_id):
    question = persistence.select_query(QSTN_TABLE, '*', ('id', '=', (qstn_id,)))
    convert_time_to_string(question)
    return question[0]


def get_answer(answ_id):
    answer = persistence.select_query(ANSW_TABLE, '*', ('id', '=', (answ_id,),))
    convert_time_to_string(answer)
    return answer[0]


def get_answers_to_question(qstn_id):
    answers = persistence.select_query(ANSW_TABLE, '*', ('question_id', '=', (qstn_id,)), 'submission_time', DESC)
    convert_time_to_string(answers)
    return answers


def get_comment(cmnt_id):
    comment = persistence.select_query(CMNT_TABLE, '*', ('id', '=', (cmnt_id,)))
    convert_time_to_string(comment)
    return comment


# Add functions
# ########################################################################
def add_new_question(new_question_input):
    new_question = {key: new_question_input[key] for key in new_question_input}
    new_question[SBMSN_TIME] = util.get_current_time()
    persistence.insert_into(
        table=QSTN_TABLE,
        columns=tuple(new_question.keys()),
        values=tuple(new_question.values())
    )


def add_new_answer(new_answer_input):
    new_answer = {key: new_answer_input[key] for key in new_answer_input}
    new_answer[SBMSN_TIME] = util.get_current_time()
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
                       where=('id', '=', (qstn_id,)))


def modify_answer(answ_id, modified_answer):

    persistence.update(table=ANSW_TABLE,
                       columns=modified_answer.keys(),
                       values=modified_answer.values(),
                       where=('id', '=', (answ_id,)))


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


def delete_comment(id_):
    persistence.delete_from_table(CMNT_TABLE, ('id', '=', (id_,)))


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
    convert_time_to_string(questions)
    return questions


def get_most_voted_question(limit):
    questions = persistence.select_query(
        QSTN_TABLE, QSTN_HEADERS, order_by='vote_number', order_type=DESC, limit=limit)
    convert_time_to_string(questions)
    return questions


def get_most_viewed_question(limit):
    questions = persistence.select_query(QSTN_TABLE, QSTN_HEADERS, order_by='view_number', order_type=DESC, limit=limit)
    convert_time_to_string(questions)
    return questions
