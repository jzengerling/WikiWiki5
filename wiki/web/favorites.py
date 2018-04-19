import sqlite3
import os
import json
import binascii
import hashlib
from functools import wraps

from flask import current_app
from flask_login import current_user


class Favorites(object):

    def __init__(self):
        return None

    def database(f):
        def _exec(self, *args, **argd):
            connection = sqlite3.connect('users.db')
            connection.execute("PRAGMA foreign_keys = ON")

            cursor = connection.cursor()

            returnVal = None

            try:
                cursor.execute('''CREATE TABLE IF NOT EXISTS Favorites 
                                 (name TEXT, page_url TEXT, 
                                 page_title TEXT, PRIMARY KEY (name, page_url), 
                                 FOREIGN KEY(name) REFERENCES Users(name))''')


                returnVal = f(self, cursor, *args, **argd)
            except Exception, e:
                connection.rollback()
                raise
            else:
                connection.commit()  # or maybe not
            finally:
                connection.close()

            return returnVal

        return _exec

    @database
    def add_favorite(self, cursor, name, url, title):
        if self.get_user(name) == None:
            return False

        cursor.execute('INSERT INTO Favorites VALUES (?,?,?)', (name, url, title))
        return True;


    @database
    def remove_favorite(self, cursor, name, url, title):

        if self.get_user(name) == None:
            return False

        cursor.execute('DELETE FROM Favorites WHERE name=? AND page_url=?', (name, url))
        if cursor.rowcount == 0:
            return False
        return True

    @database
    def get_favorites(self, cursor, name):

        if self.get_user(name) == None:
            return False

        cursor.execute('SELECT * FROM Favorites WHERE name=?', (name,))
        favorite_pages = cursor.fetchall()
        return favorite_pages


    @database
    def get_user(self, cursor, name):
        cursor.execute('SELECT * FROM Users WHERE name=?', (name,))
        user = cursor.fetchone()
        if user == None:
            return None
        else:
            cursor.execute('SELECT * FROM Roles WHERE name=?', (name,))
            roleRows = cursor.fetchall()
            roles = []
            for role in roleRows:
                roles.append(role[1])

            data = {};
            data["password"] = user[1]
            data["authenticated"] = user[2]
            data["active"] = user[3]
            data["authentication_method"] = user[4]
            data["roles"] = roles

            return User(self, user[0], data)

    def get_curret_user(self):
        user = current_user.name
        # print('user' + user)
        return user

class User(object):
    def __init__(self, manager, name, data):
        self.manager = manager
        self.name = name
        self.data = data

    def get(self, option):
        return self.data.get(option)

    def set(self, option, value):
        self.data[option] = value
        self.save()

    def save(self):
        self.manager.update(self.name, self.data)

    def is_authenticated(self):
        return self.data.get('authenticated')

    def is_active(self):
        return self.data.get('active')

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.name

