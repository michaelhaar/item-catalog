#!/usr/bin/env python3
# coding=utf8

# This file declares the mapping between our Python objects and the SQL columns
# Visit the following link for more details:
# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html

import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

DB_NAME = "itemcatalog.db"

# The `declarative_base()` base class contains a `MetaData` object where
# defined `Table` object are collected.
Base = declarative_base()

#the class is declared without any awareness of datebase
class Category(Base):
    # __tablename is a special variable that will be used to create a table
    __tablename__ = "categories"

    # map python objects to columns in our database
    id = Column(Integer, primary_key=True)
    # TODO title should be unique. Otherwise the hole urls wouldn't work.
    title = Column(String(250), nullable=False)

    #TODO add some documentation for this line
    items = relationship("Item",
                         order_by="Item.id",
                         back_populates="category")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    # TODO title should be unique. Otherwise the hole urls wouldn't work.
    title = Column(String(80), nullable=False)
    description = Column(String(250))

    # This is how we create relationships in SQLAlchemy:
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="items")


# Leave the following code lines at the end of the file:
if __name__ == "__main__":
    engine = create_engine("sqlite:///%s" % DB_NAME)
    # (The engine represents the core interface to the database)
    # Create database (if not existing) and all tables:
    Base.metadata.create_all(engine)
    print("The database has been created and can now be populated with data " +
          "by running the following command: `python populate_database.py`")
