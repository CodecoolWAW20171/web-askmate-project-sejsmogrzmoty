import persistence
import util


# ----- Table names --------------
QSTN_TABLE = 'question'
ANSW_TABLE = 'answer'
CMNT_TABLE = 'comment'
USR_TABLE = 'mate'
TAG_TABLE = 'tag'
QSTN_TAG_TABLE = 'question_tag'
MATE_TABLE = 'mate'

# ----- Column names -------------
QSTN_HEADERS = ("id",
                "submission_time",
                "view_number",
                "vote_number",
                "title",
                "message",
                "image",
                "mate_id",
                "qstn_rep",
                "accepted_answer_id")
ANSW_HEADERS = ("id",
                "submission_time",
                "vote_number",
                "question_id",
                "message",
                "image",
                "mate_id",
                "answ_rep")
CMNT_HEADERS = ("id",
                "question_id",
                "answer_id",
                "message",
                "submission_time",
                "edited_count",
                "mate_id")
USR_HEADERS = ("id",
               "username",
               "submission_time",
               "image")

# ----- Column name variables ----
(
    QSTN_ID,
    QSTN_STIME,
    QSTN_VIEWN,
    QSTN_VOTEN,
    QSTN_TITLE,
    QSTN_MSG,
    QSTN_IMG,
    QSTN_MATE,
    QSTN_REP,
    QSTN_A_ANSW
) = QSTN_HEADERS
(
    ANSW_ID,
    ANSW_STIME,
    ANSW_VOTEN,
    ANSW_QSTN_ID,
    ANSW_MSG,
    ANSW_IMG,
    ANSW_MATE,
    ANSW_REP
) = ANSW_HEADERS
(
    CMNT_ID,
    CMNT_QSTN_ID,
    CMNT_ANSW_ID,
    CMNT_MSG,
    CMNT_STIME,
    CMNT_EDIT_COUNT,
    CMNT_MATE
) = CMNT_HEADERS
(
    USR_ID,
    USR_NAME,
    USR_STIME,
    USR_PIC
) = USR_HEADERS

# ----- Default values -----------
QSTN_DEFAULTS = {QSTN_TITLE: "",
                 QSTN_MSG: "",
                 QSTN_IMG: "",
                 USR_NAME: "Anonymous"}
ANSW_DEFAULTS = {ANSW_MSG: "",
                 ANSW_IMG: "",
                 USR_NAME: "Anonymous"}
CMNT_DEFAULTS = {CMNT_MSG: "",
                 USR_NAME: "Anonymous"}
USR_DEFAULTS = {USR_NAME: "",
                USR_PIC: ""}

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
    util.switch_null_to_default(questions, QSTN_DEFAULTS, (QSTN_MATE, QSTN_A_ANSW, QSTN_REP))
    return questions


def get_question(qstn_id):
    cols = [(QSTN_TABLE, header) for header in QSTN_HEADERS]
    cols.append('username')
    join_on_cols = [(QSTN_TABLE, QSTN_MATE), (USR_TABLE, USR_ID)]
    group_by = [(QSTN_TABLE, QSTN_ID), (USR_TABLE, USR_ID)]
    where = ((QSTN_TABLE, QSTN_ID), '=', (qstn_id,))
    question = persistence.select_query(
        table=QSTN_TABLE,
        columns=cols,
        join_params=(USR_TABLE, join_on_cols, 'LEFT'),
        where=where,
        groups=group_by
    )
    util.convert_time_to_string(question, QSTN_STIME)
    util.switch_null_to_default(question, QSTN_DEFAULTS, (QSTN_MATE, QSTN_A_ANSW, QSTN_REP))
    if question:
        return question[0]
    return None


def get_answer(answ_id):
    answer = persistence.select_query(
        ANSW_TABLE, '*',
        where=(ANSW_ID, '=', (answ_id,)))
    util.convert_time_to_string(answer, ANSW_STIME)
    util.switch_null_to_default(answer, ANSW_DEFAULTS, (ANSW_MATE, ANSW_REP))
    if answer:
        return answer[0]
    return None


def get_answers_to_question(qstn_id):
    answers = persistence.get_answers_to_question(qstn_id)
    if answers:
        answers[0]['answers_number'] = len(answers)
    util.convert_time_to_string(answers, ANSW_STIME)
    util.switch_null_to_default(answers, ANSW_DEFAULTS, (ANSW_MATE,))
    return answers


def get_comment(cmnt_id):
    comment = persistence.select_query(
        CMNT_TABLE, '*',
        where=(CMNT_ID, '=', (cmnt_id,)))
    util.convert_time_to_string(comment, CMNT_STIME)
    util.switch_null_to_default(comment, CMNT_DEFAULTS, (CMNT_ANSW_ID, CMNT_QSTN_ID, CMNT_MATE))
    if comment:
        return comment[0]
    return None


def get_comments_to_question_and_answers(qstn_id, answ_ids):
    cols = [(CMNT_TABLE, header) for header in CMNT_HEADERS]
    cols.append('username')
    join_on_cols = [(CMNT_TABLE, CMNT_MATE), (USR_TABLE, USR_ID)]
    group_by = [(CMNT_TABLE, CMNT_ID), (USR_TABLE, USR_ID)]

    if answ_ids:
        where = [
                 [(CMNT_QSTN_ID, '=', (qstn_id,)),
                  (CMNT_ANSW_ID, 'IN', answ_ids)],
                 ["OR"]
                ]
    else:
        where = (CMNT_QSTN_ID, '=', (qstn_id,))

    comments = persistence.select_query(
        table=CMNT_TABLE,
        columns=cols,
        join_params=(USR_TABLE, join_on_cols, 'LEFT'),
        where=where,
        groups=group_by,
        orders=[(CMNT_STIME, DESC)]
    )
    util.convert_time_to_string(comments, CMNT_STIME)
    util.switch_null_to_default(comments, CMNT_DEFAULTS, (CMNT_ANSW_ID, CMNT_QSTN_ID, CMNT_MATE))
    return comments


def get_users_ids():
    users = persistence.select_query(
        USR_TABLE, (USR_ID, USR_NAME))
    return users


def get_user_questions(usr_id):
    return persistence.get_user_questions(usr_id)


def get_user_answers(usr_id):
    return persistence.get_user_answers(usr_id)


def get_user_comments(usr_id):
    return persistence.get_user_comments(usr_id)


def get_users_with_rep():
    users = persistence.get_users_rep()
    return users


def get_user_with_rep(usr_id):
    user = persistence.get_user_with_rep(usr_id)
    util.convert_time_to_string(user, USR_STIME)
    util.switch_null_to_default(user, USR_DEFAULTS)
    if user:
        return user[0]
    return None


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


def add_new_mate(new_input):
    add_new(MATE_TABLE, new_input, USR_STIME)


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


# Reputation
# ########################################################################
def vote_answer(answ_id, up_or_down):
    persistence.update_increment_query(
        table=ANSW_TABLE,
        column=ANSW_VOTEN,
        value=int(up_or_down),
        where=(ANSW_ID, '=', (answ_id,)))


def change_rep_qstn(qstn_id, rep_val):
    if int(rep_val) > 0:
        rep_val = int(rep_val)*5
    else:
        rep_val = int(rep_val)*-2

    persistence.update_increment_query(
        table=QSTN_TABLE,
        column=QSTN_REP,
        value=rep_val,
        where=(QSTN_ID, '=', (qstn_id,)))


def change_rep_answ(answ_id, rep_val):
    if int(rep_val) > 0:
        rep_val = int(rep_val)*10
    else:
        rep_val = int(rep_val)*-2

    persistence.update_increment_query(
        table=ANSW_TABLE,
        column=ANSW_REP,
        value=rep_val,
        where=(ANSW_ID, '=', (answ_id,)))


def change_rep_acc_answ(answ_id):
    persistence.update_increment_query(
        table=ANSW_TABLE,
        column=ANSW_REP,
        value=15,
        where=(ANSW_ID, '=', (answ_id,)))


# Accepted answer
# ########################################################################
def mark_accepted_answer(qstn_id, accepted_answer_id):
    persistence.update_query(
        table=QSTN_TABLE,
        columns=(QSTN_A_ANSW,),
        values=(accepted_answer_id,),
        where=(QSTN_ID, '=', (qstn_id,)))


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
    questions = get_all_questions(5)
    util.hide_long_string(questions, QSTN_MSG)
    return questions


def get_most_voted_question():
    questions = get_all_questions(1, [(QSTN_VOTEN, DESC)])
    util.hide_long_string(questions, QSTN_MSG)
    return questions


def get_most_viewed_question():
    questions = get_all_questions(1, [(QSTN_VIEWN, DESC)])
    util.hide_long_string(questions, QSTN_MSG)
    return questions


# Search questions
# ########################################################################
def show_searched_questions(search_phrase):
    questions = persistence.search_questions(search_phrase)
    return questions
