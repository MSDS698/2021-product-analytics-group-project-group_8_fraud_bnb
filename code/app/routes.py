from app import application, classes, db
from flask import render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_login import current_user, login_user, login_required, logout_user
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField, TextField, validators

import folium

from create_map import map_html


@application.route('/', methods=['GET'])
@application.route('/index', methods=['GET'])
@application.route('/about', methods=['GET'])
def index():
    """Index page: Renders about.html with team member names and project
    description"""
    return render_template('index.html', authenticated_user=current_user.is_authenticated)


@application.route('/search/<username>', methods=['POST', 'GET'])
@login_required
def search(username):
    listing_id_form = classes.ListIdForm()
    if listing_id_form.validate_on_submit():
        listing_id = listing_id_form.listing_id.data
        score = classes.Listings.query.filter_by(listing_id=int(listing_id)).first().listing_reliability

        if not score:
            score = 'Sorry, score not found.'

        return render_template('search_result.html',
                               listing_id=listing_id,
                               username=username,
                               score=score,
                               )

    return render_template(
        'search.html',
        username=username,
        form=listing_id_form,
    )


@application.route('/register', methods=('GET', 'POST'))
def register():
    """Register page: Renders register.html with sign up
    form asking for username, email, and password
    """
    registration_form = classes.RegistrationForm()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        password = registration_form.password.data
        email = registration_form.email.data

        user_count = classes.User.query.filter_by(username=username).count() \
            + classes.User.query.filter_by(email=email).count()
        if (user_count > 0):
            return '<h1>Error - Existing user : ' + username \
                   + ' OR ' + email + '</h1>'
        else:
            user = classes.User(username, email, password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html', form=registration_form)


@application.route('/login', methods=['GET', 'POST'])
def login():
    """Login page: Renders login.html with submit
    form for username and password
    """
    login_form = classes.LogInForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user = classes.User.query.filter_by(username=username).first()

        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))

    return render_template('login.html', form=login_form)


@application.route('/logout')
@login_required
def logout():
    """Logout page: Unauthorized server error (expected)
    """
    logout_user()
    return redirect(url_for('index'))


@application.route('/reliability-map')
@login_required
def display_1000_listing():
    return map_html(1000)


@application.route('/reliability-map/<max_listing>')
@login_required
def display_n_listing(max_listing):
    return map_html(max_listing)

@application.route('/dashboard')
@login_required
def fake_dashboard():
    return render_template(
        'dashboard.html',
        authenticated_user=current_user.is_authenticated,
        not_at_index=True,
    )