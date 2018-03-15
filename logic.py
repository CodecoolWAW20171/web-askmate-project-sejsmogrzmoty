import persistence
import util


# ----- Constants -----
QSTN_HEADERS = ["id", "submisson_time", "view_number", "vote_number", "title", "message", "image"]
ANSW_HEADERS = ["id", "submisson_time", "vote_number", "question_id", "message", "image"]


def get_all_questions():
    questions = persistence.get_data_from_file(persistence.QSTN_FILE_PATH)
    for question in questions:
        question['answers_number'] = count_how_many_answers(question['id'])
    return questions


def get_answers_to_question(qstn_id):
    answers = persistence.get_data_from_file(persistence.ANSW_FILE_PATH)
    listed_answers = []
    for answer in answers:
        if answer['question_id'] == qstn_id:
            listed_answers.append(data)
    return listed_answers


def count_how_many_answers(qstn_id):
    answers = persistence.get_data_from_file(persistence.ANSW_FILE_PATH)
    counter = 0
    for answer in answers:
        if answer["question_id"] == qstn_id:
            counter += 1
    return counter


def add_new_question(question):
    questions = persistence.get_data_from_file(persistence.QSTN_FILE_PATH)
    questions.append(question)
    return persistence.write_data_to_file(questions, persistence.QSTN_FILE_PATH)


def modify_question(qstn_id, modified_question):
    questions = persistence.get_data_from_file(persistence.QSTN_FILE_PATH)
    for question in questions:
        if question['id'] == qstn_id:
            for header in QSTN_HEADERS:
                question[header] = modified_question[header]
            question['answers_number'] = count_how_many_answers(question['id'])
            return questions


def add_answer(answer):
    answers = persistence.get_data_from_file(persistence.QSTN_FILE_PATH)
    answers.append(answer)
    return persistence.write_data_to_file(answers, persistence.ANSW_FILE_PATH)


def delete_question(qstn_id):
    # Writes an updated list of questions to the csv file
    question_data = persistence.get_data_from_file("question.csv")
    persistence.write_data_to_file([question for question in question_data if question['id'] != qstn_id], "question.csv")

    # Writes an updated list of answers to the csv file
    answer_data = persistence.get_data_from_file("answer.csv")
    persistence.write_data_to_file([answer for answer in answer_data if answer['question_id'] != qstn_id], "answer.csv")


'''
Removes a specified answer from csv file

Args:
        answer id
Returns:
        None
        writes to csv the updated lists of dictionaries
'''


def delete_answer(answ_id):
    answer_data = persistence.get_data_from_file("answer.csv")
    updated_answers = [[answer for answer in answer_data if answer['id'] != answ_id]]
    return updated_answers


# Helper function in database management
# ########################################################################
def generate_new_id(data):
    pass


def find_id_index(data, id_):
    pass


def code_string(dictionary, header, key):
    """
    Transcoding dictionary value to or from base64.

    Args:
        dictionary: dictionary
        header: Dictionary header
        key: Type of cryptography

    Returns:
        Decoded/encoded string
    """
    if header in ["title", "message", "image"]:
        if key == "encode":
            return str(base64.b64encode(bytes(dictionary[header], "utf-8")))[2:-1]
        elif key == "decode":
            return base64.b64decode(bytes(dictionary[header], "utf-8")).decode("utf-8")
        else:
            raise ValueError("Wrong key!")
    else:
        return dictionary[header]
