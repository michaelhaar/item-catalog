#!/usr/bin/env python3
# coding=utf8

"""
This file/module basically defines the database tables, their structure and
creates the database if it doesn't exist.

HOW IT WORKS:
Our relational database tables are defined through Python classes!! :)
Instances of these classes will then represent the single rows in our database
tables.

Note:
The official SQLAlchemy documentation is a bit overwhelming IMHO. Therefore I'm
providing the relevant parts for this file below:
http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/basic_use.html
http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html
http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
"""

import sys
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

DB_NAME = "itemcatalog.db"

# The `declarative_base()` base class contains a `MetaData` object where
# defined `Table` object are collected.
Base = declarative_base()


class Category(Base):
    # __tablename__ is a special variable that will be used for the tablename
    __tablename__ = "categories"

    # define the columns of this table:
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False, unique=True)
    # 'bidirectional One-To-Many'-relationship
    items = relationship("Item",
                         order_by="Item.id",
                         back_populates="category")
    # Note:
    # I made the title unique. This makes it possible to find category entries
    # through it's title. I'd argue that this assumption absolutely valid,
    # because otherwise the required url routings wouldn't work at all!?


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    g_user_id = Column(String, nullable=True, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)


class Item(Base):
    # specify the tablename
    __tablename__ = "items"
    # Declare it's columns
    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False, unique=True)
    description = Column(String(250))
    # This is how we create 'One-To-Many'-relationships in SQLAlchemy:
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="items")
    creator_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category.id': self.category_id
        }


# Leave the following code lines at the end of the file:
engine = create_engine("postgresql://catalog:topsecret@localhost/catalogdb")
# (The engine represents the core interface to the database)
# Finally create database (if not existing) and all tables:
Base.metadata.create_all(engine)
