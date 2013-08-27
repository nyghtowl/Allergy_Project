from flask import render_template, flash, redirect, session, url_for, request, jsonify, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from forms import LoginForm, EditProfile, SearchForm
from models import User
from config 

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

@app.before_request
def before_request():
    g.user = current_user

    # Updated database with the last time user seen
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

# @app.after_request
# def after_request(response):
#     for query in get_debug_queries():
#         if query.duration >= DATABASE_QUERY_TIMEOUT:
#             app.logger.warning('SLOW QUERY: %s\nParameters: %s\nDuration: %fs\Context: %s\n') % (query.statement, query.parameters, query.duration, query.context)
#     return response

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
def login():
    form = LoginForm()

    # Validate login
    if form.validate_on_submit():
        user = User.query.filter(User.email==form.email.data).first()
 
        # If user exists then apply login user functionatlity to generate current_user session
        if user is not None:
            user_password = user.password
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('search'))
        else:
            flash('Your email or password are incorrect. Please login again.')
    return render_template('login.html', form=form)

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