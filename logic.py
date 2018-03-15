import persistence
import util


# ----- Constants -----
QSTN_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
QSTN_DEFAULTS = {"view_number": 0, "vote_number": 0, "title": "", "message": "", "image": ""}
ANSW_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]


def get_all_questions():
    questions = persistence.get_data_from_file(persistence.QSTN_FILE_PATH)
    for question in questions:
        question['answers_number'] = count_how_many_answers(question['id'])
        question['submission_time'] = util.convert_timestamp(int(question['submission_time']))
    return questions


def get_answers_to_question(qstn_id):
    answers = persistence.get_data_from_file(persistence.ANSW_FILE_PATH)
    listed_answers = []
    for answer in answers:
        if answer['question_id'] == qstn_id:
            listed_answers.append(data)
    return listed_answers


def get_question(qstn_id):
    questions = persistence.get_data_from_file(persistence.QSTN_FILE_PATH)
    for question in questions:
        if question['id'] == qstn_id:
            return question


def count_how_many_answers(qstn_id):
    answers = persistence.get_data_from_file(persistence.ANSW_FILE_PATH)
    counter = 0
    for answer in answers:
        if answer["question_id"] == qstn_id:
            counter += 1
    return counter


def add_new_question(new_question_input):
    questions = persistence.get_data_from_file(persistence.QSTN_FILE_PATH)
    question = {header: new_question_input[header] for header, dvalue in QSTN_DEFAULTS.items() if header in new_question_input}
    question["id"] = generate_new_id(questions)
    question['submission_time'] = util.get_current_timestamp()
    questions.append(question)
    return persistence.write_data_to_file(questions, persistence.QSTN_FILE_PATH, QSTN_HEADERS)


def modify_question(qstn_id, modified_question):
    questions = persistence.get_data_from_file(persistence.QSTN_FILE_PATH)
    for question in questions:
        if question['id'] == qstn_id:
            for header in QSTN_HEADERS:
                question[header] = modified_question[header]
            question['answers_number'] = count_how_many_answers(question['id'])
            return questions


def add_answer(answer):
    answers = persistence.get_data_from_file(persistence.ANSW_FILE_PATH)
    answer["id"] = generate_new_id(answers)
    answer['submission_time'] = util.get_current_timestamp()
    answers.append(answer)
    return persistence.write_data_to_file(answers, persistence.ANSW_FILE_PATH, ANSW_HEADERS)


def delete_question(qstn_id):
    # Writes an updated list of questions to the csv file
    question_data = persistence.get_data_from_file(persistence.QSTN_FILE_PATH)
    persistence.write_data_to_file(
        [question for question in question_data if question['id'] != qstn_id],
        persistence.QSTN_FILE_PATH,
        QSTN_HEADERS)

    # Writes an updated list of answers to the csv file
    answer_data = persistence.get_data_from_file(persistence.ANSW_FILE_PATH)
    persistence.write_data_to_file(
        [answer for answer in answer_data if answer['question_id'] != qstn_id],
        persistence.ANSW_FILE_PATH,
        ANSW_HEADERS)


def delete_answer(answ_id):
    '''
    Removes a specified answer from csv file

    Args:
            answer id
    Returns:
            None
            writes to csv the updated lists of dictionaries
    '''
    answer_data = persistence.get_data_from_file(persistence.ANSW_FILE_PATH)
    updated_answers = [[answer for answer in answer_data if answer['id'] != answ_id]]
    return updated_answers


# Helper function in database management
# ########################################################################
def generate_new_id(data):
    new_id = 0
    for entry in data:
        new_id = entry['id']
    return new_id + 1


def find_id_index(data, id_):
    index = 0
    for entry in data:
        if entry['id'] == id_:
            return index
        else:
            index += 1


def sort_by(data, header, ascending=False):
    return sorted(data, key=lambda x: x[header], reverse=ascending)


def vote_question(id_, up_or_down):
    all_data = persistence.get_data_from_file(persistence.QSTN_FILE_PATH)
    all_data = change_vote(id_, all_data, up_or_down)
    persistence.write_data_to_file(all_data, persistence.QSTN_FILE_PATH, QSTN_HEADERS)


def vote_answer(id_, up_or_down):
    all_data = persistence.get_data_from_file(persistence.ANSW_FILE_PATH)
    all_data = change_vote(id_, all_data, up_or_down)
    persistence.write_data_to_file(all_data, persistence.ANSW_FILE_PATH, ANSW_HEADERS)


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
            if up_or_down == "down":
                data["vote_number"] -= 1
        return all_data
