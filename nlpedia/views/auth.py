# coding=utf-8
from flask import Blueprint, redirect, url_for, request, session, flash, render_template
from nlpedia.models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if len(username) < 3:
            flash('Your username must be at least 3 characters.')
        elif len(password) < 5:
            flash('Your password must be at least 5 characters.')
        elif not User(username).register(password):
            flash('A user with that username already exists.')
        else:
            session['username'] = username
            flash('Logged in.')

            return redirect(url_for('index'))

    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not User(username).verify_password(password):
            flash('Invalid login.')
        else:
            session['username'] = username

            # TODO: Remove the following line after the experiment
            session['number_of_posts_viewed'] = 0

            flash('Logged in.')

            return redirect(url_for('index'))

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.pop('username')
    # TODO: Remove the following line after the experiment
    session.pop('number_of_posts_viewed')
    flash('Logged out.')
    return redirect(url_for('index'))