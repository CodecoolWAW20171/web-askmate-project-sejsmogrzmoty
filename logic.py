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


def delete_comment_of_question(qstn_id):
    persistence.delete_from_table(CMNT_TABLE, ('question_id', '=', (qstn_id,)))


def delete_comment_of_answer(answ_id):
    persistence.delete_from_table(CMNT_TABLE, ('answer_id', '=', (answ_id,)))


# Helper function in database management
# ########################################################################
def count_how_many_answers(qstn_id):
    answers = get_all_answers()
    counter = 0
    for answer in answers:
        if answer["question_id"] == qstn_id:
            counter += 1
    return counter


def find_id_index(data, id_):
    for e, entry in enumerate(data):
        if entry['id'] == id_:
            return e


def count_answered_questions():
    pass


# Sorting
# ########################################################################
def sort_by(data, header, descending=True):
    return sorted(data, key=lambda x: x[header], reverse=descending)


def get_sorted_questions(header, descending=True):
    questions = get_all_questions()
    for question in questions:
        question['answers_number'] = count_how_many_answers(question['id'])
    questions = sort_by(questions, header, descending)
    for question in questions:
        question['submission_time'] = util.convert_timestamp(int(question['submission_time']))
    return questions


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


def change_vote(id_, all_data, up_or_down):
    '''
    Changes the vote_number of a specified answer/question

    Args:
            id:
                id of the voted question
                type: int

            up_or_down:
                "up" or "down" depending on whether you're upvoting or downvoting
                type: str

    Returns:
            None
            writes to csv the updated lists of dictionaries
    '''
    for data in all_data:
        if data["id"] == id_:
            if up_or_down == "up":
                data["vote_number"] += 1
            elif up_or_down == "down":
                data["vote_number"] -= 1
            return all_data


# Counting views
# ########################################################################
def increase_view_counter(id_):
    questions = get_all_questions()
    found_index = find_id_index(questions, id_)
    if found_index is None:
        return
    questions[found_index]['view_number'] += 1
    write_all_questions_to_file(questions)


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
