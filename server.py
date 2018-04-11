from flask import Flask, render_template, request, redirect, url_for, abort

import logic


app = Flask(__name__)


# Home
# ########################################################################
@app.route('/')
def route_index():

    # Display home page

    top_question_titles = ("The most recent questions",
                           "The most viewed question",
                           "The top voted question")
    most_recent = logic.get_most_recent_questions()
    most_viewed = logic.get_most_viewed_question()
    top_voted = logic.get_most_voted_question()
    top_questions = list(zip(top_question_titles, (most_recent, most_viewed, top_voted)))

    return render_template('index.html', top_questions=top_questions)


# List
# ########################################################################
@app.route('/list')
def list_questions():

    # Display a page with questions list

    questions = logic.get_all_questions()

    return render_template('list.html', questions=questions)


# Search
# ########################################################################
@app.route('/search')
def list_searched_questions():

    search_phrase = request.args.get('search')
    questions = logic.show_searched_questions(search_phrase)
    return render_template('list_searched.html', search_phrase=search_phrase, questions=questions)


# View question
# ########################################################################
@app.route('/question/<int:qstn_id>')
def show_question(qstn_id):

    # Display a page with a single question

    logic.increase_view_counter(qstn_id)
    question = logic.get_question(qstn_id)
    if question is None:
        abort(404)
    answers = logic.get_answers_to_question(qstn_id)
    answers_ids = [answer[logic.ANSW_ID] for answer in answers]
    comments = logic.get_comments_to_question_and_answers(qstn_id, answers_ids)
    return render_template('detail.html', question=question, answers=answers, comments=comments)


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

    question = logic.get_question(qstn_id)
    if question is None:
        abort(404)
    answer = logic.ANSW_DEFAULTS

    return render_template('ans_form.html', form_type='new', answer=answer, question=question)


# About
# ########################################################################
@app.route('/about')
def about():

    # Display some 'about' page with info about the application

    return render_template('about.html')


# Error message
# ########################################################################
@app.errorhandler(404)
def page_not_found(e):

    # Display error page

    return render_template('error_page.html'), 404


# <------------------------------ ____ --------------------------------------->


# Edit question
# ########################################################################
@app.route('/question/edit', methods=['POST'])
def edit_question():

    # Receive form request with the question id and send request to logic
    # to retrive question data.
    # Display a page with the form filled with the question existing data

    qstn_id = int(request.form['id'])
    question = logic.get_question(qstn_id)

    return render_template('q_form.html', form_type="edit", question=question)


# Delete question
# ########################################################################
@app.route('/question/delete', methods=['POST'])
def delete_question():

    qstn_id = int(request.form['id'])
    logic.delete_question(qstn_id)

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

    question = request.form
    if qstn_id is None:
        logic.add_new_question(question)
    else:
        logic.modify_question(qstn_id, question)

    return redirect(url_for('list_questions'))


# Edit answer
# ########################################################################
@app.route('/answer/edit', methods=['POST'])
def edit_answer():

    # Receive form request with the answer id and send request to logic
    # to retrive answer data.
    # Display a page with the form filled with the answer existing data

    answ_id = int(request.form['id'])
    qstn_id = int(request.form['question_id'])
    answer = logic.get_answer(answ_id)
    question = logic.get_question(qstn_id)

    return render_template('ans_form.html', form_type="edit", answer=answer, question=question)


# Delete answer
# ########################################################################
@app.route('/answer/delete', methods=['POST'])
def delete_answer():

    # Receive form request with the answer id and send request to logic
    # to delete the answer from the database.
    # Redirect to the page with the question after successful deletion

    answ_id = int(request.form['id'])
    qstn_id = int(request.form['question_id'])
    logic.delete_answer(answ_id)

    return redirect(url_for('show_question', qstn_id=qstn_id))


# Request to modify answer database
# ########################################################################
@app.route('/answer', methods=['POST'])
@app.route('/answer/<int:answ_id>', methods=['POST'])
def modify_answer_database(answ_id=None):

    # Receive form request with the new data filled by the user and send
    # request to logic to modify the database incorporating the new data
    # Redirect to the page with the question after successful
    # database modification

    answer = request.form
    qstn_id = answer['question_id']
    if answ_id is None:
        logic.add_new_answer(answer)
    else:
        logic.modify_answer(answ_id, answer)

    return redirect(url_for('show_question', qstn_id=qstn_id))


# Vote
# ########################################################################
@app.route('/question/<int:qstn_id>/vote', methods=['POST'])
def vote_question(qstn_id):

    vote = request.form['vote']
    logic.vote_question(qstn_id, vote)

    return redirect(url_for('show_question', qstn_id=qstn_id))


@app.route('/answer/<int:answ_id>/vote', methods=['POST'])
def vote_answer(answ_id):

    vote = request.form['vote']
    answer = logic.get_answer(answ_id)
    qstn_id = answer['question_id']
    logic.vote_answer(answ_id, vote)

    return redirect(url_for('show_question', qstn_id=qstn_id))


# Modify comment database
# ########################################################################
@app.route('/question/save-comment', methods=['POST'])
@app.route('/question/save-comment/<int:cmnt_id>', methods=['POST'])
def modify_comment_to_question(cmnt_id=None):

    comment = request.form
    qstn_id = comment['question_id']
    if cmnt_id is None:
        logic.add_new_comment(comment)
    else:
        logic.modify_comment(cmnt_id, comment)

    return redirect(url_for('show_question', qstn_id=qstn_id))


@app.route('/answer/save-comment', methods=['POST'])
@app.route('/answer/save-comment/<int:cmnt_id>', methods=['POST'])
def modify_comment_to_answer(cmnt_id=None):

    comment = request.form
    answ_id = comment['answer_id']
    answer = logic.get_answer(answ_id)
    qstn_id = answer['question_id']
    if cmnt_id is None:
        logic.add_new_comment(comment)
    else:
        logic.modify_comment(cmnt_id, comment)

    return redirect(url_for('show_question', qstn_id=qstn_id))


@app.route('/question/<int:qstn_id>/new-comment')
def post_comment_to_question(qstn_id):

    # Displays a page with a question and a form to be filled with
    # the new comment

    question = logic.get_question(qstn_id)
    if question is None:
        abort(404)
    comment = logic.CMNT_DEFAULTS

    return render_template('cmnt_q_form.html', form_type='new', comment=comment, question=question)


@app.route('/answer/<int:answ_id>/new-comment')
def post_comment_to_answer(answ_id):

    # Displays a page with a question and form to be filled with
    # the new comment

    answer = logic.get_answer(answ_id)
    if answer is None:
        abort(404)
    comment = logic.CMNT_DEFAULTS

    return render_template('cmnt_a_form.html', form_type='new', comment=comment, answer=answer)


@app.route('/question/<int:qstn_id>/edit-comment', methods=['POST'])
def edit_question_comment(qstn_id):

    cmnt_id = request.form['id']
    question = logic.get_question(qstn_id)
    comment = logic.get_comment(cmnt_id)
    if question is None or comment is None:
        abort(404)

    return render_template('cmnt_q_form.html', form_type='edit', comment=comment, question=question)


@app.route('/answer/<int:answ_id>/edit-comment', methods=['POST'])
def edit_answer_comment(answ_id):

    cmnt_id = request.form['id']
    answer = logic.get_answer(answ_id)
    comment = logic.get_comment(cmnt_id)
    if answer is None or comment is None:
        abort(404)

    return render_template('cmnt_a_form.html', form_type='edit', comment=comment, answer=answer)


@app.route('/<int:cmnt_id>/delete-comment-answer', methods=['POST'])
def delete_comment_answer(cmnt_id):

    answ_id = request.form['answer_id']
    answer = logic.get_answer(answ_id)
    qstn_id = answer['question_id']
    logic.delete_comment(cmnt_id)

    return redirect(url_for('show_question', qstn_id=qstn_id))


@app.route('/<int:cmnt_id>/delete-comment-question', methods=['POST'])
def delete_comment_question(cmnt_id):

    qstn_id = request.form['question_id']
    logic.delete_comment(cmnt_id)

    return redirect(url_for('show_question', qstn_id=qstn_id))
    

# <------------------------------ ____ --------------------------------------->


# Mate database
# ########################################################################
@app.route('/mates')
def mates_list():
    mates = logic.get_users()
    return render_template('mates_list.html', mates = mates)


@app.route('/mates/<int:mate_id>')
def show_mate(mate_id=0):
    mate = logic.get_user(mate_id)[0]
    print(mate)
    return render_template('mate.html', mate=mate)

@app.route('/registration')
def register():
    return render_template('new-mate.html')

@app.route('/registration', methods=['POST'])
def add_new_mate():
    mate = request.form
    logic.add_new_mate(mate)
    return redirect(url_for('mates_list'))

# Run server
# ########################################################################
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
