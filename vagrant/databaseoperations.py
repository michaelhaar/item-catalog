#!/usr/bin/env python3
# coding=utf8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item


def db_create(session):
    # create an instance of the restaurant class
    my_first_restaurant = Restaurant(name="Pizza Palace")
    # add the restaurant to the "staging zone"
    session.add(my_first_restaurant)
    # make the changes persistant
    session.commit()

    # The following line tells us that something has been created
    # print(session.query(Restaurant).all())

    # Let's add a MenuItem to our new restaurant
    cheesepizza = MenuItem(name="Cheese Pizza",
                           description="""Made with all natural ingredients and
                           fresh mozzarella""",
                           course="Entree",
                           price="$8.99",
                           restaurant=my_first_restaurant)
    session.add(cheesepizza)
    session.commit()
    # The following line tells us that something has been created
    # print(session.query(MenuItem).all())


def db_read(session):
    # Querying the database can be done through the ".query(..)" method.
    # the ".first()" will give us an object that represents the first row in
    # that table.
    first_result = session.query(Restaurant).first()
    print(first_result.name)

    # ".all()" will give us a list of restaurant objects
    restaurants = session.query(Restaurant).all()
    for restaurant in restaurants:
        print(restaurant.name+"\n")

    # more query commands can be found here:
    # http://docs.sqlalchemy.org/en/rel_0_9/orm/query.html


def print_veggie_burgers(session):
    # This is a small helper function to the db_update() function
    veggie_burgers = session.query(MenuItem).filter_by(name="Veggie Burger")
    for veggie_burger in veggie_burgers:
        print(veggie_burger.id)
        print(veggie_burger.name)
        print(veggie_burger.price)
        print(veggie_burger.restaurant.name)
        print("\n")


def db_update(session):
    # In this example we want to update the price of the "Veggie Burger"
    # of the restaurant called "Urban Burger".
    # First we need to find the corresponding entry:
    print_veggie_burgers(session)
    # by looking at the output, we now know that we have to update the
    # entry with id=8.

    urban_veggie_burger = session.query(MenuItem).filter_by(id=8).one()
    print(urban_veggie_burger.price)
    # Let's finally update the price :)
    urban_veggie_burger.price = "$2.99"
    session.add(urban_veggie_burger)
    session.commit()

    print_veggie_burgers(session)


def db_delete(session):
    # Assume that we want to delete "Auntie Ann's Dinner'"s spinach ice cream
    # We need to find the corresponding entry first:
    spinach_ice_cream = session.query(MenuItem).filter_by(name="Spinach Ice Cream").one()
    print(spinach_ice_cream.restaurant.name)
    # It's the correct one, because it's from "Auntie Ann's Diner'"
    session.delete(spinach_ice_cream)
    session.commit()

    # If we are now searching form the spinach ice cream we should get
    # a NoResultFound error, because we deleted that entry
    spinach_ice_cream = session.query(MenuItem).filter_by(name="Spinach Ice Cream").one()
    print(spinach_ice_cream.restaurant.name)


def create_category(session, name):
    pass

class DatabaseOperations:
    """TODO: add docstring here """


    def __init__(self):
        # Connect to the database.
        # (The engine represents the core interface to the database)
        engine = create_engine('sqlite:///itemcatalog.db')
        # Don't know exactly what this line does
        Base.metadata.bind = engine
        # Create a sessionmaker object,
        # (This object acts like a factory for producing new sessions)
        db_session = sessionmaker(bind=engine)
        # The ORM’s “handle” to the database is the Session object
        self.session = db_session()


    def add_item(self):
        pass


    def add_category(self, cat_name):
        # create an instance of the category class
        cat_soccer = Category(name=cat_name)
        # add the category to the "staging zone"
        self.session.add(cat_soccer)
        # make the changes persistant
        self.session.commit()


    def get_categories(self):
        # Querying the database can be done through the ".query(..)" method.
        # ".all()" will give us a list of restaurant objects
        categories = self.session.query(Category).all()
        for category in categories:
            print(category.name+"\n")

        # more query commands can be found here:
        # http://docs.sqlalchemy.org/en/rel_0_9/orm/query.html




if __name__ == "__main__":
    db = DatabaseOperations()

    db.add_category("Soccer")
    db.add_category("Icehockey")
    db.get_categories()
