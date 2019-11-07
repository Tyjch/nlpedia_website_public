# coding=utf-8
from flask import Blueprint, redirect, url_for, request, session, flash, render_template
from nlpedia.models.user import User
from nlpedia.models.content import (get_todays_recent_facts,
                                    get_todays_recent_questions,
                                    get_fact_from_id,
                                    get_question_from_id,
                                    get_fact_tags_from_id,
                                    get_question_tags_from_id,
                                    connect_nodes,
                                    get_related_facts,
                                    get_related_questions)

# This is disabled while using Heroku's free tier
# from nlpedia.models.nlp import extract_tags

bp = Blueprint('content', __name__, url_prefix='/content')

# FACTS ================================================================================================================

@bp.route('/add_fact', methods=['GET','POST'])
def add_fact():

    if request.method == 'POST':
        title = request.form['title']
        tags  = request.form['tags']
        text  = request.form['text']

        if not title:
            flash('You must give your fact a title.')
        elif not tags:
            flash('You must give your fact at least one tag.')
        elif not text:
            flash('You must give your fact a text body.')
        else:
            # This is disabled while using Heroku's free tier
            # tags = tags + extract_tags(text)
            User(session['username']).add_fact(title, tags, text)

        return redirect(url_for('index'))

    return render_template('facts/add_fact.html')

@bp.route('/display_facts')
def display_facts():
    facts = get_todays_recent_facts()
    return render_template(
        'facts/display_facts.html',
        facts=facts
    )

@bp.route('/view_fact/<fact_id>')
def view_fact(fact_id):
    current_username = session.get('username')

    if current_username:
        current_user = User(current_username)
        current_user.view_fact(fact_id)

    fact = get_fact_from_id(fact_id)

    return render_template(
        'facts/view_fact.html',
        fact=fact,
        related_facts=get_related_facts('Fact', fact_id),
        related_questions=get_related_questions('Fact', fact_id)
    )

@bp.route('/edit_fact/<fact_id>', methods=['GET', 'POST'])
def edit_fact(fact_id):

    fact = get_fact_from_id(fact_id)
    data = fact.data()

    title = data[0]['fact']['title']
    tags = ', '.join(get_fact_tags_from_id(fact_id).data()[0]['tags'])
    text = data[0]['fact']['text'].lstrip()

    if request.method == 'POST':
        title = request.form['title']
        tags = request.form['tags']
        text = request.form['text']

        if not title:
            flash('You must give your fact a title.')
        elif not tags:
            flash('You must give your fact at least one tag.')
        elif not text:
            flash('You must give your fact a text body.')
        else:
            # This is disabled while using Heroku's free tier
            # tags = tags + extract_tags(text)
            User(session['username']).edit_fact(fact_id, title, tags, text)

        return redirect(url_for('index'))

    return render_template(
        'facts/edit_fact.html',
        fact_id=fact_id,
        fact=fact,
        title=title,
        tags=tags,
        text=text
    )

@bp.route('/delete_fact/<fact_id>')
def delete_fact(fact_id):
    current_username = session.get('username')

    if current_username:
        current_user = User(current_username)
        current_user.delete_fact(fact_id)

    return redirect(url_for('index'))

# QUESTIONS ============================================================================================================

@bp.route('/add_question', methods=['GET', 'POST'])
def add_question():

    if request.method == 'POST':
        title = request.form['title']
        tags  = request.form['tags']
        text  = request.form['text']
        answer = request.form['answer']

        if not title:
            flash('You must give your question a title.')
        elif not tags:
            flash('You must give your question at least one tag.')
        elif not text:
            flash('You must give your question a text body.')
        elif not answer:
            flash('You must give your question an answer.')
        else:
            # This is disabled while using Heroku's free tier
            # tags = tags + extract_tags(text)
            User(session['username']).add_question(title, tags, text, answer)

        return redirect(url_for('index'))

    return render_template('questions/add_question.html')

@bp.route('/display_questions')
def display_questions():
    questions = get_todays_recent_questions()
    return render_template(
        'questions/display_questions.html',
        questions=questions
    )

# TODO
@bp.route('/view_question/<question_id>')
def view_question(question_id):
    current_username = session.get('username')

    if current_username:
        current_user = User(current_username)
        current_user.view_question(question_id)

    question = get_question_from_id(question_id)

    return render_template(
        'questions/view_question.html',
        question=question,
        related_facts=get_related_facts('Question', question_id),
        related_questions=get_related_questions('Question', question_id)
    )

@bp.route('/edit_question/<question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    question = get_question_from_id(question_id)
    data = question.data()

    title = data[0]['question']['title']
    tags = ', '.join(get_question_tags_from_id(question_id).data()[0]['tags'])
    text = data[0]['question']['text'].lstrip()
    answer = data[0]['question']['answer'].lstrip()

    if request.method == 'POST':
        title = request.form['title']
        tags = request.form['tags']
        text = request.form['text']
        answer = request.form['answer']

        if not title:
            flash('You must give your question a title.')
        elif not tags:
            flash('You must give your question at least one tag.')
        elif not text:
            flash('You must give your question a text body.')
        elif not answer:
            flash('You must give your question an answer.')
        else:
            # This is disabled while using Heroku's free tier
            # tags = tags + extract_tags(text)
            User(session['username']).edit_question(question_id, title, tags, text, answer)

        return redirect(url_for('index'))

    return render_template(
        'questions/edit_question.html',
        question_id = question_id,
        question=question,
        title=title,
        tags=tags,
        text=text,
        answer=answer
    )

@bp.route('/delete_question/<question_id>')
def delete_question(question_id):
    current_username = session.get('username')

    if current_username:
        current_user = User(current_username)
        current_user.delete_question(question_id)

    return redirect(url_for('index'))

@bp.route('/answer_question/<question_id>', methods=['POST'])
def answer_question(question_id):
    if request.method == 'POST':
        answer = request.form['answer']

        if not answer:
            flash('You must answer this question')
        else:
            User(session['username']).answer_question(question_id, answer)

    return redirect(request.referrer)


# TODO
@bp.route('/answer_correct/<question_id>', methods=['POST'])
def answer_correct(question_id):
    current_username = session.get('username')

    if current_username:
        current_user = User(current_username)
        current_user.answer_correct(question_id)

    return redirect(url_for('index'))

# TODO
@bp.route('/answer_incorrect/<question_id>', methods=['POST'])
def answer_incorrect(question_id):
    current_username = session.get('username')

    if current_username:
        current_user = User(current_username)
        current_user.answer_incorrect(question_id)

    return redirect(url_for('index'))

# FEEDBACK =============================================================================================================

@bp.route('/feedback/<primary_label>/<user_feedback>/<node_id>', methods=['GET', 'POST'])
def feedback(primary_label, node_id, user_feedback):
    current_username = session.get('username')

    if current_username:
        current_user = User(current_username)
        current_user.give_feedback(primary_label, node_id, user_feedback)

    return redirect(request.referrer)

# OTHER ================================================================================================================

@bp.route('/connect', methods=['GET', 'POST'])
def connect():
    if request.method == 'POST':
        label1 = request.form['label1']
        id1 = request.form['id1']
        label2 = request.form['label2']
        id2 = request.form['id2']

        connect_nodes(id1, label1, id2, label2)

        return redirect(request.referrer)

    return render_template('connect.html')