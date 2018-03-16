import persistence
import util


# ----- Constants -----------
QSTN_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSW_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]

# ----- Column indecies -----
QSTN_ID, QSTN_STIME, QSTN_VIEWN, QSTN_VOTEN, QSTN_TITLE, QSTN_MSG, QSTN_IMG = range(len(QSTN_HEADERS))
ANSW_ID, ANSW_STIME, ANSW_VOTEN, ANSW_QSTN_ID, ANSW_MSG, ANSW_IMG = range(len(ANSW_HEADERS))

# ----- Default values ------
QSTN_DEFAULTS = {"view_number": 0, "vote_number": 0, "title": "", "message": "", "image": ""}
ANSW_DEFAULTS = {"vote_number": 0, "message": "", "image": ""}


# Get functions
# ########################################################################
def get_all_questions():
    questions = persistence.get_data_from_file(persistence.QSTN_FILE_PATH)
    return questions


def get_all_answers():
    answers = persistence.get_data_from_file(persistence.ANSW_FILE_PATH)
    return answers


def get_all_answers_converted():
    answers = get_all_answers()
    for a, answer in enumerate(answers):
        answers[a]['submission_time'] = util.convert_timestamp(int(answer['submission_time']))
    return answers


def get_question(qstn_id):
    questions = get_all_questions()
    for question in questions:
        if question['id'] == qstn_id:
            question['submission_time'] = util.convert_timestamp(int(question['submission_time']))
            question['answers_number'] = count_how_many_answers(question['id'])
            return question


def get_answer(answ_id):
    answers = get_all_answers_converted()
    for answer in answers:
        print(answer)
        if answer['id'] == answ_id:
            return answer


def get_answers_to_question(qstn_id):
    answers = get_all_answers_converted()
    listed_answers = []
    for answer in answers:
        if answer['question_id'] == qstn_id:
            listed_answers.append(answer)
    return listed_answers


# Write functions
# ########################################################################
def write_all_questions_to_file(questions):
    persistence.write_data_to_file(questions, persistence.QSTN_FILE_PATH, QSTN_HEADERS)


def write_all_answers_to_file(answers):
    persistence.write_data_to_file(answers, persistence.ANSW_FILE_PATH, ANSW_HEADERS)


# Add functions
# ########################################################################
def add_new_question(new_question_input):
    questions = get_all_questions()
    new_question = util.prepare_new_entry(questions, new_question_input, QSTN_DEFAULTS)
    questions.append(new_question)
    write_all_questions_to_file(questions)


def add_new_answer(new_answer_input):
    answers = get_all_answers()
    new_answer = util.prepare_new_entry(answers, new_answer_input, ANSW_DEFAULTS)
    new_answer['question_id'] = new_answer_input['question_id']
    answers.append(new_answer)
    write_all_answers_to_file(answers)


# Modify question database
# ########################################################################
def modify_question(qstn_id, modified_question):
    questions = get_all_questions()
    for question in questions:
        if question['id'] == qstn_id:
            for header in QSTN_HEADERS:
                if header in modified_question:
                    question[header] = modified_question[header]
    write_all_questions_to_file(questions)


def modify_answer(answ_id, modified_answer):
    answers = get_all_answers()
    for answer in answers:
        if answer['id'] == answ_id:
            for header in ANSW_HEADERS:
                if header in modified_answer:
                    answer[header] = modified_answer[header]
            answer['question_id'] = modified_answer['question_id']
    write_all_answers_to_file(answers)


def delete_question(qstn_id):
    # Writes an updated list of questions to the csv file
    question_data = get_all_questions()
    questions_filtered = [question for question in question_data if question['id'] != qstn_id]
    write_all_questions_to_file(questions_filtered)

    # Writes an updated list of answers to the csv file
    answer_data = get_all_answers()
    answers_filtered = [answer for answer in answer_data if answer['question_id'] != qstn_id]
    write_all_answers_to_file(answers_filtered)


def delete_answer(answ_id):
    '''
    Removes a specified answer from csv file

    Args:
            answer id
    Returns:
            None
            writes to csv the updated lists of dictionaries
    '''
    answer_data = get_all_answers()
    updated_answers = [answer for answer in answer_data if answer['id'] != answ_id]
    write_all_answers_to_file(updated_answers)


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
    questions = get_all_questions()
    questions = change_vote(id_, questions, up_or_down)
    write_all_questions_to_file(questions)


def vote_answer(id_, up_or_down):
    answers = get_all_answers()
    answers = change_vote(id_, answers, up_or_down)
    write_all_answers_to_file(answers)


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
def get_top_questions():
    top_questions = []

    questions = get_sorted_questions('submission_time')
    top_questions.append(questions[0])
    questions = sort_by(questions, 'view_number')
    top_questions.append(questions[0])
    questions = sort_by(questions, 'vote_number')
    top_questions.append(questions[0])

    return top_questions
