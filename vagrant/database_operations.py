#!/usr/bin/env python3
# coding=utf8

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Item, User

DB_NAME = "itemcatalog.db"


class DatabaseOperations:
    """
    This class implements the database CRUD-operations.
    """

    def __init__(self):
        """ This funtion creates the `Session` object. """
        # Connect to the database.
        # (The engine represents the core interface to the database)
        engine = create_engine("postgresql://catalogUser:topsecret@localhost/catalog")
        # Create a sessionmaker object.
        # (This object acts like a factory for producing new sessions)
        db_session = sessionmaker(bind=engine)
        # The `Session` object is our “handle” to the database. We love it <3
        # see: http://docs.sqlalchemy.org/en/latest/orm/session_basics.html
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

    def add_user(self, auth_session):
        user = User(g_user_id=auth_session['g_user_id'],
                    name=auth_session['name'],
                    email=auth_session['email'])
        self.session.add(user)
        self.session.commit

    def get_user_by_guserid(self, g_user_id):
        return self.session.query(User).filter_by(g_user_id=g_user_id).one()

    def register_user(self, auth_session):
        guserid = auth_session['g_user_id']
        if self.session.query(User).filter_by(g_user_id=guserid).count() > 0:
            # user is already registered
            return False
        else:
            self.add_user(auth_session)
            return True

    def user_authorization(self, itm_title, auth_session):
        item = self.get_item_by_title(itm_title)
        if item.creator.g_user_id == auth_session['g_user_id']:
            return True
        else:
            # The user is not the creator of the item and therefore not
            # authorized to make changes.
            return False

    def item_count(self):
        return self.session.query(Item).count()

    def add_item(self, itm_title, itm_description, cat_title, auth_session):
        itm_category = self.get_category_by_title(cat_title)
        itm_creator = self.get_user_by_guserid(auth_session['g_user_id'])
        item = Item(title=itm_title,
                    description=itm_description,
                    category=itm_category,
                    creator=itm_creator)
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
