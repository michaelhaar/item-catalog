#!/usr/bin/env python3
# coding=utf8

"""
This file will fill the database with some sample entries if there aren't any
"""

from database_operations import DatabaseOperations

db = DatabaseOperations()

# If there aren't any categories, add the following categories to the database
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
print("The following categories are now available in the database:")
for category in categories:
    print("- " + category.title)


# Let's try to add some items to the database, if there aren't any
description_placeholder = "Lorem ipsum dolor sit amet, consetetur sadipscing"
if db.item_count() == 0:
    db.add_item("Stick", description_placeholder, "Hockey")
    db.add_item("Goggles", description_placeholder, "Snowboarding")
    db.add_item("Snowboard", description_placeholder, "Snowboarding")
    db.add_item("Frisbee", description_placeholder, "Frisbee")
    db.add_item("Bat", description_placeholder, "Baseball")
    db.add_item("Two shinguards", description_placeholder, "Soccer")
    db.add_item("Shinguards", description_placeholder, "Soccer")
    db.add_item("Jersey", description_placeholder, "Soccer")
    db.add_item("Soccer Cleats", description_placeholder, "Soccer")

# Print soccer items
soccer_items = db.get_items_of_category("Soccer")
print("You'll need the following items if you wanna play soccer:")
for soccer_item in soccer_items:
    print("- " + soccer_item.title)
