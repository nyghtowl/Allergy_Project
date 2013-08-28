from flask import render_template, flash, redirect, session, url_for, request, jsonify, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import get_debug_queries
from app import app, db, login_manager, oid
from forms import LoginForm, EditProfile, SearchForm
from models import User, ROLE_USER, ROLE_ADMIN
from config import DATABASE_QUERY_TIMEOUT

# Load user from database
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

# Hook before reques to check user loggged in
@app.before_request
def before_request():
    g.user = current_user

    # Updated database with the last time user seen
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form=SearchForm()

# Hook after each request that checks if alerts needed
@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= DATABASE_QUERY_TIMEOUT:
            app.logger.warning('SLOW QUERY: %s\nParameters: %s\nDuration: %fs\Context: %s\n') % (query.statement, query.parameters, query.duration, query.context)
    return response

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler #oid
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('login'))
    
    form = LoginForm()

    # Validate login
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email']) 

    return render_template('login.html', form=form, providers = app.config['OPENID_PROVIDERS'])


# Triggered after oid.try_login
@oid.after_login
def after_login(resp):
    # If no email then cannot login
    if resp.email is None or resp.email == "":
        flash(gettext('Invalid login. Please try again.'))
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()

    # If email is not found then treat like new user and generate nickname from email
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_valid_nickname(nickname)
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()

    remember_me = False

    # Check session remember_me and login user
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    flash('Logged in successfully.')


    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
@login_required # Confirms login
def logout():
    logout_user()
    flash('You are now logged out')
    return redirect(url_for('index'))


@app.route('/create_profile', methods = ['POST', 'GET'])
def create_profile():
    form = EditProfile()

    if form.validate_on_submit():

        user = User.query.filter(User.email==form.email.data).first()

        if user != None:
            user_email = user.email
            if user_email == form.email.data:
                flash ('%(email)s already exists. Please login or enter a different email.', email = user_email)
                return redirect(url_for('login'))
        # If user doesn't exist, save from data in User object to commit to db
        if user == None:
            new_user = User(id = None,
                        email=form.email.data,
                        password=form.password.data,
                        fname=form.fname.data,
                        lname=form.lname.data,
                        mobile=form.mobile.data,
                        zipcode=form.zipcode.data,
                        accept_tos=True,
                        timestamp=time.time())
            db.session.add(new_user)
            db.session.commit()
            flash('Account creation successful. Please login to your account.')
            return redirect(url_for('index'))
    return render_template('create_login.html', form=form)

# Search shell
@app.route('/search', methods=['POST'])
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query = g.search_form.search.data))

@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    txt_so_far = None

    # Pull letters entered so far
    if request.method == 'POST':
        txt_so_far = str(request.form['msg'])

    # Lookup locations to recommend based on prefix
    if txt_so_far:
        # Search for allergies and return most frequently used
        # based on each letter typed
        pass

    return json.dumps({ "options": predictions})

@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = 'test'
    return render_template('search_results.html',
        query = query,
        results = results)