#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    manage.py
    ---------------

    Manage module
"""

from app.core import manager, db


@manager.command
def create():
    print('Creating all of the tables in the database...')
    db.create_all()


@manager.command
def drop():
    print('Dropping all of the tables from the database...')
    db.drop_all()


if __name__ == "__main__":
    manager.run()
