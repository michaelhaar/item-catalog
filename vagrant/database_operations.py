#!/usr/bin/env python3
# coding=utf8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
import os


# def db_create(session):
#     # create an instance of the restaurant class
#     my_first_restaurant = Restaurant(name="Pizza Palace")
#     # add the restaurant to the "staging zone"
#     session.add(my_first_restaurant)
#     # make the changes persistant
#     session.commit()
#
#     # The following line tells us that something has been created
#     # print(session.query(Restaurant).all())
#
#     # Let's add a MenuItem to our new restaurant
#     cheesepizza = MenuItem(name="Cheese Pizza",
#                            description="""Made with all natural ingredients and
#                            fresh mozzarella""",
#                            course="Entree",
#                            price="$8.99",
#                            restaurant=my_first_restaurant)
#     session.add(cheesepizza)
#     session.commit()
#     # The following line tells us that something has been created
#     # print(session.query(MenuItem).all())
#
#
# def db_read(session):
#     # Querying the database can be done through the ".query(..)" method.
#     # the ".first()" will give us an object that represents the first row in
#     # that table.
#     first_result = session.query(Restaurant).first()
#     print(first_result.name)
#
#     # ".all()" will give us a list of restaurant objects
#     restaurants = session.query(Restaurant).all()
#     for restaurant in restaurants:
#         print(restaurant.name+"\n")
#
#     # more query commands can be found here:
#     # http://docs.sqlalchemy.org/en/rel_0_9/orm/query.html
#
#
# def print_veggie_burgers(session):
#     # This is a small helper function to the db_update() function
#     veggie_burgers = session.query(MenuItem).filter_by(name="Veggie Burger")
#     for veggie_burger in veggie_burgers:
#         print(veggie_burger.id)
#         print(veggie_burger.name)
#         print(veggie_burger.price)
#         print(veggie_burger.restaurant.name)
#         print("\n")
#
#
# def db_update(session):
#     # In this example we want to update the price of the "Veggie Burger"
#     # of the restaurant called "Urban Burger".
#     # First we need to find the corresponding entry:
#     print_veggie_burgers(session)
#     # by looking at the output, we now know that we have to update the
#     # entry with id=8.
#
#     urban_veggie_burger = session.query(MenuItem).filter_by(id=8).one()
#     print(urban_veggie_burger.price)
#     # Let's finally update the price :)
#     urban_veggie_burger.price = "$2.99"
#     session.add(urban_veggie_burger)
#     session.commit()
#
#     print_veggie_burgers(session)
#
#
# def db_delete(session):
#     # Assume that we want to delete "Auntie Ann's Dinner'"s spinach ice cream
#     # We need to find the corresponding entry first:
#     spinach_ice_cream = session.query(MenuItem).filter_by(name="Spinach Ice Cream").one()
#     print(spinach_ice_cream.restaurant.name)
#     # It's the correct one, because it's from "Auntie Ann's Diner'"
#     session.delete(spinach_ice_cream)
#     session.commit()
#
#     # If we are now searching form the spinach ice cream we should get
#     # a NoResultFound error, because we deleted that entry
#     spinach_ice_cream = session.query(MenuItem).filter_by(name="Spinach Ice Cream").one()
#     print(spinach_ice_cream.restaurant.name)

DB_NAME = "itemcatalog.db"

class DatabaseOperations:
    """
    This class implements the database CRUD-operations.

    Note: Make sure that the database has already been created by running
    the following command in your vagrant machine:
    `python database_setup.py`.
    """

    def __init__(self):
        """ This funtion creates the `Session` object. """
        # Connect to the database.
        # (The engine represents the core interface to the database)
        engine = create_engine('sqlite:///%s' % DB_NAME)
        # TODO Don't know exactly what this line does
        # TODO Base.metadata.bind = engine
        # Create a sessionmaker object,
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
        """ returns the category object that has the given title. """
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



    def get_latest_items(self):
        #TODO This can be deleted!?
        return self.session.query(Item).limit(5)

    def get_item_by_title(self, cat_title, itm_title):
        """ returns the category object that has the given title. """
        #TODO the category check isn't necessary
        category = self.get_category_by_title(cat_title)
        return self.session.query(Item).filter_by(category=category, title=itm_title).one()
