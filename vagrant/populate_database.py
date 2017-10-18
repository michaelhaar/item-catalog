#!/usr/bin/env python3
# coding=utf8

from database_operations import DatabaseOperations

db = DatabaseOperations()

# Add the following categories to the database if no categories exits
if db.category_count() == 0:
    db.add_category("Soccer")
    db.add_category("Basketball")
    db.add_category("Baseball")
    db.add_category("Frisbee")
    db.add_category("Snowboarding")
    db.add_category("Rock Climbing")
    db.add_category("Foosball")
    db.add_category("Skating")
    db.add_category("Hockey")

# Display available categories
categories = db.get_categories()
for category in categories:
    print(category.name+"\n")


# Let's try to create an Item
cat_soccer = db.get_category_by_name("Soccer")
db.add_item("Ball","Best ball ever",cat_soccer)
db.add_item("Shoes","Old shoes from Lionel Messi",cat_soccer)
db.add_item("21 Friends","Some friends to play with",cat_soccer)
db.add_item("Field","The larger the better",cat_soccer)
soccer_items = db.get_items_of_category("Soccer")
for soccer_item in soccer_items:
    print(soccer_item.title)
    print(soccer_item.description)
    print(soccer_item.category.name)
