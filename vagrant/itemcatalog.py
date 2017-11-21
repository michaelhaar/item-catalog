#!/usr/bin/env python3
# coding=utf8

"""
This file/module implements the main part of our Flask webserver.

Important resources for understanding this file are listed below.
Flask: (Python Webserver Framework)
    - http://flask.pocoo.org/docs/0.12/quickstart/   <-- READ THIS FIRST!!
    - http://flask.pocoo.org/docs/0.12/quickstart/#rendering-templates
    - http://flask.pocoo.org/docs/0.12/quickstart/#sessions
Jinja2 templates:
    - (http://jinja.pocoo.org/docs/2.9/templates/)
Google-Signin part (for user authentication):
    - https://developers.google.com/identity/sign-in/web/devconsole-project
    - https://developers.google.com/identity/sign-in/web/sign-in
    - https://developers.google.com/identity/sign-in/web/backend-auth
"""

import uuid
import json
import flask
from flask import Flask, render_template
from google.oauth2 import id_token
from google.auth.transport import requests
from database_operations import DatabaseOperations

app = Flask(__name__)

# Note: Flask's `session` objects are build on top of cookies and are signed
# cryptographically. Therefore we need a secret key. --> This means that
# Users can read the content of our cookie, but not modify it.
# See: http://flask.pocoo.org/docs/0.12/quickstart/#sessions
app.secret_key = str(uuid.uuid4())

# Our main database object
db = DatabaseOperations()

# This variable specifies the name of a file that contains the Google's OAuth
# information for this application, including its client_id and client_secret.
CLIENT_ID = '713304857721-r72atdutco08u548b1ru6ujmt0lfod0n.apps.googleusercontent.com'  # noqa


@app.route('/')
@app.route('/catalog')
def show_categories():
    """ Shows a list of all categories """
    # return 'Hello, World!'    <-- Basic usage

    # returning HTML websites as Python strings is not very convenient.
    # It's far better to use Flask's `render_template()` function and
    # Jinja2 templates, which are really awesome.
    # see: http://flask.pocoo.org/docs/0.12/quickstart/#rendering-templates
    return render_template('categories.html',
                           page_heading="Catalog App",
                           categories=db.get_categories())


@app.route('/catalog/<category_name>/items')
def show_items(category_name):
    """ Displays a list of all items in this category """
    return render_template('items.html',
                           page_heading=category_name + ' Items',
                           items=db.get_items_of_category(category_name),
                           category=category_name)


@app.route('/catalog/<category_name>/<item_name>')
def show_item(category_name, item_name):
    """ Returns the item's detail page """
    return render_template('item.html',
                           page_heading=item_name,
                           item=db.get_item_by_title(item_name))


@app.route('/catalog/<category_name>/add', methods=['GET', 'POST'])
def add_item(category_name):
    if 'g_user_id' not in flask.session:
        # User is not authenticated
        return flask.redirect(flask.url_for('show_categories'))

    if flask.request.method == 'POST':
        # receive values from html form
        # TODO do we need some security checks to deny XSS or SQL injection!?
        item_title = flask.request.form['item-title']
        item_desc = flask.request.form['item-desc']
        # store item in our database
        db.add_item(item_title, item_desc, category_name, flask.session)
        # redirect/forward to the items list of this category
        return flask.redirect(flask.url_for(
            'show_items',
            category_name=category_name))
    else:
        # GET Request --> render form
        return render_template("add_item.html",
                               category=category_name)


@app.route('/catalog/<item_name>/edit', methods=['GET', 'POST'])
def edit_item(item_name):
    if 'g_user_id' not in flask.session:
        # User is not authenticated
        return flask.redirect(flask.url_for('show_categories'))
    if db.user_authorization(item_name, flask.session) is False:
        # User is not authorized to make changes
        return flask.redirect(flask.url_for('show_categories'))

    if flask.request.method == 'POST':
        # receive values from html form
        # TODO do we need some security checks? --> XSS, SQL-injection
        new_title = flask.request.form['new-title']
        new_desc = flask.request.form['new-desc']
        new_category = flask.request.form['new-category']
        # update database
        db.update_item(item_name, new_title, new_desc, new_category)
        # redirect/forward to items detail page
        return flask.redirect(flask.url_for(
            'show_item',
            category_name=new_category,
            item_name=new_title))
    else:
        # GET Request --> render form
        return render_template("edit_item.html",
                               item=db.get_item_by_title(item_name),
                               categories=db.get_categories())


@app.route('/catalog/<item_name>/delete', methods=['GET', 'POST'])
def del_item(item_name):
    if 'g_user_id' not in flask.session:
        # User is not authenticated
        return flask.redirect(flask.url_for('show_categories'))
    if db.user_authorization(item_name, flask.session) is False:
        # User is not authorized to make changes
        return flask.redirect(flask.url_for('show_categories'))

    if flask.request.method == 'POST':
        # find the item's category
        cat_of_item = db.get_item_by_title(item_name).category.title
        # delete the item from the database
        db.delete_item(item_name)
        # redirect/forward to the items list of this category
        return flask.redirect(flask.url_for(
            'show_items',
            category_name=cat_of_item))
    else:
        # GET Request --> render the delete confirmation form
        return render_template("delete_item.html",
                               item=db.get_item_by_title(item_name))


@app.route('/catalog.JSON')
def getCatalog():
    """ Returns a JSON version of the catalog """
    output_json = []
    categories = db.get_categories()
    for category in categories:
        items = db.get_items_of_category(category.title)
        category_output = {}
        category_output["id"] = category.id
        category_output["name"] = category.title
        category_output["items"] = [i.serialize for i in items]
        output_json.append(category_output)
    return flask.jsonify(Categories=output_json)


# GOOGLE SIGN-IN PART:
@app.route('/logout')
def logout():
    flask.session.pop('g_user_id', None)
    flask.session.pop('name', None)
    flask.session.pop('email', None)
    flask.session.pop('logged_in', None)
    return "You are logged out!"


@app.route('/login')
def login():
    return render_template('login.html',
                           client_id=CLIENT_ID,
                           tokensignin_url=flask.url_for('gconnect'))


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Get the ID token from the request
    token = flask.request.form["idtoken"]
    # Verify the integrity of the ID token
    idinfo = verifyIdToken(token)
    if idinfo is None:
        return responseWith("Invalid ID Token", 401)

    # ID token is valid.
    # Get the user's Google Account ID from the decoded token.
    flask.session['g_user_id'] = idinfo['sub']
    flask.session['name'] = idinfo['name']
    flask.session['email'] = idinfo['email']
    flask.session['logged_in'] = True
    db.register_user(flask.session)
    return responseWith("ID Token is valid", 200)


def verifyIdToken(token):
    try:
        # verify the token's signature, the `aud` (=audience) claim, and
        # the `exp`-claim (=expiry time).
        idinfo = id_token.verify_oauth2_token(token,
                                              requests.Request(),
                                              CLIENT_ID)
        # verify the `iss`-claim (iss=issuer).
        valid_issuers = ['accounts.google.com', 'https://accounts.google.com']
        if idinfo['iss'] not in valid_issuers:
            raise ValueError('Wrong issuer.')
        # ID token is valid.
        return idinfo
    except ValueError:
        # Invalid token
        return None


def responseWith(message, response_code):
    response = flask.make_response(json.dumps(message), response_code)
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == '__main__':
    # enable debug support --> server will reload itself on code changes
    app.debug = True

    # By default the Flask server is only accessible from the host machine and
    # not from any other computer.
    # Since we are using a Vagrant environment (=virtual machine), we must make
    # our server publicly available. This is done with the following line:
    app.run(host='0.0.0.0', port=5000)
