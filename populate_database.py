#!/usr/bin/env python3
# coding=utf8

"""
This file will fill the database with some sample categories if there aren't any
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
