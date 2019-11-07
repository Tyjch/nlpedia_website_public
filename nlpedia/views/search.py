# coding=utf-8
from flask import Blueprint, redirect, url_for, request, session, flash, render_template
from nlpedia.models.search import (get_facts_by_title,
                                   get_facts_by_tag,
                                   get_facts_by_text,
                                   get_questions_by_title,
                                   get_questions_by_tag,
                                   get_questions_by_text)

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/search_facts', methods=['GET', 'POST'])
def search_facts():
    return render_template('facts/search_facts.html')

@bp.route('/search_facts_by_title', methods=['GET', 'POST'])
def search_facts_by_title():
    posts = []

    if request.method == 'POST':
        title = request.form['title']

        if not title:
            flash('You must enter a title.')
        else:
            posts = get_facts_by_title(title)

    return render_template(
        'facts/search_results.html',
        posts=posts
    )

@bp.route('/search_facts_by_tag', methods=['GET', 'POST'])
def search_facts_by_tag():
    posts = []

    if request.method == 'POST':
        tag = request.form['tag']

        if not tag:
            flash('You must enter a tag.')
        else:
            posts = get_facts_by_tag(tag)

    return render_template(
        'facts/search_results.html',
        posts=posts
    )

@bp.route('/search_facts_by_text', methods=['GET', 'POST'])
def search_facts_by_text():
    posts = []

    if request.method == 'POST':
        text = request.form['text']

        if not text:
            flash('You must enter text.')
        else:
            posts = get_facts_by_text(text)

    return render_template(
        'facts/search_results.html',
        posts=posts
    )

@bp.route('/search_questions', methods=['GET', 'POST'])
def search_questions():
    return render_template('questions/search_questions.html')

@bp.route('/search_questions_by_title', methods=['GET', 'POST'])
def search_questions_by_title():
    posts = []

    if request.method == 'POST':
        title = request.form['title']

        if not title:
            flash('You must enter a title.')
        else:
            posts = get_questions_by_title(title)

    return render_template(
        'questions/search_results.html',
        posts=posts
    )

@bp.route('/search_questions_by_tag', methods=['GET', 'POST'])
def search_questions_by_tag():
    posts = []

    if request.method == 'POST':
        tag = request.form['tag']

        if not tag:
            flash('You must enter a tag.')
        else:
            posts = get_questions_by_tag(tag)

    return render_template(
        'questions/search_results.html',
        posts=posts
    )

@bp.route('/search_questions_by_text', methods=['GET', 'POST'])
def search_questions_by_text():
    posts = []

    if request.method == 'POST':
        text = request.form['text']

        if not text:
            flash('You must enter text.')
        else:
            posts = get_questions_by_text(text)

    return render_template(
        'questions/search_results.html',
        posts=posts
    )