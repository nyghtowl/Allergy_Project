# Config
# -*- coding: utf-8 -*-

import os

from signal import signal, SIGPIPE, SIG_DFL 
#Ignore SIG_PIPE and don't throw exceptions on it... (http://docs.python.org/library/signal.html)
signal(SIGPIPE,SIG_DFL) 

SECRET_KEY = 'key'
# SECRET_KEY = os.environ.get('key')

CSRF_ENABLED = True

basedir = os.path.abspath(os.path.dirname(__file__))
# s3_basedir = 'http://s3.amazonaws.com/allergymerlin/'

# Code to setup a postgres database
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/allergy_db'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

# Stores migrate data files
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Use get_debug_queries function
SQLALCHEMY_RECORD_QUERIES = True

# Threashold for slow loading (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }
