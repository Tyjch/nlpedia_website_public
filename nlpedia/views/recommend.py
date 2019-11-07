# coding=utf-8
# coding=utf-8
from flask import Blueprint, redirect, url_for, request, session, flash, render_template
from nlpedia.models.recommend import naive_rule
from passlib.hash import bcrypt

bp = Blueprint('recommend', __name__, url_prefix='/recommend')


@bp.route('/naive_rule')
def recommend_post():
    random_node=[]
    current_username = session.get('username')

    if current_username:
        random_record = naive_rule(current_username)

        try:
            len_record = len(random_record)

            # The following is used for the experiment only
            session['number_of_posts_viewed'] += 1
            if session['number_of_posts_viewed'] >= 40:
                secret_code = bcrypt.encrypt(current_username)
                return render_template(
                    'recommend/naive_rule.html',
                    message=f'You have already viewed all posts. If you are coming from Amazon Mturk, your secret code is {secret_code}'
                )

        except TypeError:
            secret_code = bcrypt.encrypt(current_username)
            return render_template(
                'recommend/naive_rule.html',
                message=f'You have already viewed all posts. If you are coming from Amazon Mturk, your secret code is {secret_code}'
            )

        if len_record >= 1:
            random_node = random_record['post']
            if random_node:
                if random_node.has_label('Fact'):
                    return redirect(url_for('content.view_fact', fact_id=random_node['id']))
                elif random_node.has_label('Question'):
                    return redirect(url_for('content.view_question', question_id=random_node['id']))


    return render_template(
        'recommend/naive_rule.html',
        message='You must be logged in to use this feature.'
    )
