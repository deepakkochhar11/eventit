#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import send_from_directory, abort
import datetime
from flask_login import login_required
from app import login_manager, app, admin, db
from models import User, Event, Connection
from admin import EventitAdminModelView, UserModelView
import views


login_manager.init_app(app)
login_manager.login_view = 'login'

admin.add_view(UserModelView(User, db.session))
admin.add_view(EventitAdminModelView(Event, db.session))
admin.add_view(EventitAdminModelView(Connection, db.session))


@login_manager.user_loader
def load_user(_id):
    from models import User
    return User.query.get(int(_id))


# Configure templates
JINJA2_GLOBALS = {
    'now': datetime.datetime.now
}
app.jinja_env.globals.update(**JINJA2_GLOBALS)


@app.before_request
def get_current_user():
    pass


@app.route('/page/<path:filename>')
def pages(filename):
    if app.config['PAGES_PATH']:
        return send_from_directory(app.config['PAGES_PATH'], filename)
    abort(404)


@app.route('/user_page/<path:filename>')
@login_required
def user_pages(filename):
    if app.config['USER_PAGES_PATH']:
        return send_from_directory(app.config['USER_PAGES_PATH'], filename)
    abort(404)