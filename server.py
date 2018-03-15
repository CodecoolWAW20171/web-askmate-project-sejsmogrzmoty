from flask import Flask, render_template, request, redirect, url_for, session

import logic
import persistence


app = Flask(__name__)


# Home
# ########################################################################
@app.route('/')
def route_index():

    # Display home page

    return render_template('index.html')


# List
# ########################################################################
@app.route('/list')
def list_questions():

    # Display a page with questions list

    questions = logic.get_all_questions()

    return render_template('list.html', questions=questions)


# View question
# ########################################################################
@app.route('/question/<int:qstn_id>')
def show_question(qstn_id):

    # Display a page with a single question

    question = logic.get_question(qstn_id)
    answers = logic.get_answers_to_question(qstn_id)

    return render_template('detail.html', question=question, answers=answers)


# Ask question
# ########################################################################
@app.route('/new-question')
def ask_question():

    # Displays a page with a form to be filled with the new question
    question = logic.QSTN_DEFAULTS

    return render_template('q_form.html', form_type="new", question=question)


# Post answer
# ########################################################################
@app.route('/question/<int:qstn_id>/new-answer')
def post_answer(qstn_id):

    # Displays a page with a question and a form to be filled with
    # the new answer

    return


# About
# ########################################################################
@app.route('/about')
def about():

    # Display some 'about' page with info about the application

    return


# <------------------------------ ____ --------------------------------------->


# Edit question
# ########################################################################
@app.route('/question/edit', methods=['POST'])
def edit_question():

    # Receive form request with the question id and send request to logic
    # to retrive question data.
    # Display a page with the form filled with the question existing data

    qstn_id = int(request.form['id'])

    return redirect(url_for('show_question', qstn_id=qstn_id))


# Delete question
# ########################################################################
@app.route('/question/delete', methods=['POST'])
def delete_question():
    result = request.form
    logic.delete_question(result["id"])
    return redirect(url_for('list_questions'))


# Request to modify question database
# ########################################################################
@app.route('/question', methods=['POST'])
@app.route('/question/<int:qstn_id>', methods=['POST'])
def modify_question_database(qstn_id=None):

    # Receive form request with the new data filled by the user and send
    # request to logic to modify the database incorporating the new data
    # Redirect to the page with the question list after successful
    # database modification

    return


# Edit answer
# ########################################################################
@app.route('/answer/edit', methods=['POST'])
def edit_answer():

    # Receive form request with the answer id and send request to logic
    # to retrive answer data.
    # Display a page with the form filled with the answer existing data

    return


# Delete answer
# ########################################################################
@app.route('/answer/delete', methods=['POST'])
def delete_answer():

    # Receive form request with the answer id and send request to logic
    # to delete the answer from the database.
    # Redirect to the page with the question after successful deletion

    return


# Run server
# ########################################################################
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
