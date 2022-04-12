from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
# import re

# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Recipe:
    db = "recipe_sm"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.date_made = data['date_made']
        self.under_thirty = data['under_thirty']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def create_recipe(cls , data):
        query = "INSERT INTO recipes(name, description, instruction, date_made, under_thirty, user_id) VALUES(%(name)s, %(description)s, %(instruction)s, %(date_made)s, %(under_thirty)s, %(user_id)s)"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query="SELECT * FROM recipes"
        results = connectToMySQL(cls.db).query_db(query)
        recipes = []
        for row in results:
            recipes.append(cls(row))
        return recipes

    @classmethod
    def get_one(cls, data):
        query="SELECT * FROM recipes JOIN users ON user_id = users.id WHERE recipes.id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        row = results[0]
        recipe = cls(row)
        user_data = {
            'id' : row['users.id'],
            'first_name' : row['first_name'],
            'last_name' : row['last_name'],
            'email' : row['email'],
            'password' : row['password'],
            'created_at' : row['users.created_at'],
            'updated_at' : row['users.updated_at']
        }
        user = User(user_data)
        recipe.user = user
        return recipe

    @classmethod
    def update(cls, data):
        query="UPDATE recipes SET name=%(name)s, description=%(description)s, instruction=%(instruction)s, date_made=%(date_made)s, under_thirty=%(under_thirty)s WHERE id=%(id)s; "
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query="DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)


    @staticmethod
    def validate_recipe(recipe):
        isValid = True
        if len(recipe['name']) < 2:
            flash("Name must be at least 3 characters")
            isValid = False
        if len(recipe['description']) < 2:
            flash("Description must be at least 3 characters")
            isValid = False
        if len(recipe['instruction']) < 2:
            flash("Instructions must be at least 3 characters")
            isValid = False
        if recipe['date_made'] == "":
            flash("Please enter a date")
            isValid = False
        return isValid

