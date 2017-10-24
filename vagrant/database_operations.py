#!/usr/bin/env python3
# coding=utf8

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Item

DB_NAME = "itemcatalog.db"


class DatabaseOperations:
    """
    This class implements the database CRUD-operations.
    """

    def __init__(self):
        """ This funtion creates the `Session` object. """
        # Connect to the database.
        # (The engine represents the core interface to the database)
        engine = create_engine('sqlite:///%s' % DB_NAME)
        # Create a sessionmaker object.
        # (This object acts like a factory for producing new sessions)
        db_session = sessionmaker(bind=engine)
        # The `Session` object is our “handle” to the database. We love it <3
        self.session = db_session()

    def add_category(self, cat_title):
        # create an instance of the category class
        category = Category(title=cat_title)
        # add the category to the "staging zone"
        self.session.add(category)
        # make the changes persistant
        self.session.commit()

    def get_categories(self):
        # Querying the database can be done through the ".query(..)" method.
        # ".all()" will give us a python list of Category objects.
        # more query commands can be found at:
        # http://docs.sqlalchemy.org/en/latest/orm/query.html
        return self.session.query(Category).all()

    def get_category_by_title(self, cat_title):
        """ returns the category object that belongs to the provided title. """
        return self.session.query(Category).filter_by(title=cat_title).one()

    def category_count(self):
        return self.session.query(Category).count()

    def item_count(self):
        return self.session.query(Item).count()

    def add_item(self, itm_title, itm_description, cat_title):
        itm_category = self.get_category_by_title(cat_title)
        item = Item(title=itm_title,
                    description=itm_description,
                    category=itm_category)
        self.session.add(item)
        self.session.commit()

    def get_items_of_category(self, cat_title):
        category = self.get_category_by_title(cat_title)
        return self.session.query(Item).filter_by(category=category).all()

    def get_item_by_title(self, itm_title):
        """ returns the item object that belongs to the provided title. """
        return self.session.query(Item).filter_by(title=itm_title).one()

    def update_item(self, current_title, new_title, new_desc, new_category):
        # First we need to find the item object:
        item = self.get_item_by_title(current_title)
        # Update the values:
        item.title = new_title
        item.description = new_desc
        item.category = self.get_category_by_title(new_category)
        # Make the changes persistant
        self.session.add(item)
        self.session.commit()

    def delete_item(self, itm_title):
        item = self.get_item_by_title(itm_title)
        self.session.delete(item)
        self.session.commit()
