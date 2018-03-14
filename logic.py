import persistence
import util


# ----- Constants -----
QSTN_HEADERS = ['id', 'submisson_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSW_HEADERS = ['id', 'submisson_time', 'vote_number', 'question_id', 'message', 'image']


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


def delete_question(qstn_id):
    pass


def delete_answer(answ_id):
    pass


# Helper function in database management
# ########################################################################
def generate_new_id(data):
    pass


def find_id_index(data, id_):
    pass
