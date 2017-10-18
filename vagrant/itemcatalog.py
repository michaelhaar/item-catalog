#!/usr/bin/env python3
# coding=utf8

from flask import Flask, render_template
from database_operations import DatabaseOperations
app = Flask(__name__)
db = DatabaseOperations()

@app.route('/')
def index():
    return render_template('main.html',
                            categories=db.get_categories(),
                            list_group_title='Latest Items',
                            items=db.get_latest_items())

@app.route('/catalog/<category_name>/items')
def show_category(category_name):
    items = db.get_items_of_category(category_name)
    list_title = category_name + ' Items'
    list_title += ' (' + str(len(items)) + ' items)'
    return render_template('main.html',
                            categories=db.get_categories(),
                            list_group_title=list_title,
                            items=db.get_items_of_category(category_name))

@app.route('/catalog/<category_name>/<item_title>')
def show_item(category_name, item_title):
    item = db.get_item_by_title(category_name, item_title)
    return render_template('item.html',
                            item=item)


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port=5000)
