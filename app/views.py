from flask import render_template, flash, redirect, session, url_for, request, jsonify, g
from app import db, app, login_manager
from flask.ext.login import login_user, logout_user, current_user, login_required
from models import Location, User
from forms import LoginForm, CreateLogin


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')