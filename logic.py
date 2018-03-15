import persistence
import util


# ----- Constants -----
QSTN_HEADERS = ["id", "submisson_time", "view_number", "vote_number", "title", "message", "image"]
ANSW_HEADERS = ["id", "submisson_time", "vote_number", "question_id", "message", "image"]


def get_all_questions():
    pass


def get_answers_to_question(qstn_id):
    pass


def add_new_question(question):
    pass


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
