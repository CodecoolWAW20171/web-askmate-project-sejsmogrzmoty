import persistence
import util


# ----- Constants -----
QSTN_HEADERS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
ANSW_HEADERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]


def get_all_questions():
    return persistence.get_data_from_file("question.csv")


def get_answers_to_question(qstn_id):
    complete_data = persistence.get_data_from_file("answer.csv")
    listed_answers = []
    for data in complete_data:
        if data['question_id'] == qstn_id:
            listed_answers.append(data)
    return listed_answers


def add_new_question(question):
    return persistence.write_data_to_file(question, "question.txt")


def modify_question(qstn_id, question):
    pass


def add_answer_to_question(qstn_id, answer):
    pass

'''
-->  zakłada, że write_data_to_file nadpisuje istniejący plik  <--
Removes a specified question and all its answers from csv files

Args:
        question id
Returns:
        None
        writes to csv the updated lists of dictionaries
'''
def delete_question(qstn_id):
    # Writes an updated list of questions to the csv file
    question_data = persistence.get_data_from_file("question.csv")
    persistence.write_data_to_file([question for question in question_data if question['id'] != qstn_id], "question.csv" )

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
    # for dictionary in data:
    pass



def find_id_index(data, id_):
    pass
