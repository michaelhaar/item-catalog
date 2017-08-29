import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Category(Base):
    # __tablename is a special variable that will be used to create a table
    __tablename__ = "categories"

    # map python objects to columns in our database
    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)

    items = relationship("Item",
                         order_by=Address.id,
                         back_populates="categories")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    description = Column(String(250))

    # create relationships in SQLAlchemy:
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="items")


# insert at the end of the file
engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.create_all(engine)
