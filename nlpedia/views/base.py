# coding=utf-8
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from nlpedia.models.user import User

bp = Blueprint('base', __name__, url_prefix='/base')

@bp.route('/profile/<username>')
def profile(username):
    user = User(username)
    facts = user.get_recent_facts()
    questions = user.get_recent_questions()

    return render_template(
        'profile.html',
        username=username,
        facts=facts,
        questions=questions
    )


