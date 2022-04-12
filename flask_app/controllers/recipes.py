from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe



@app.route('/dashboard')
def dashboard():
    user_data = {
        'id' : session["user_id"]
    }
    return render_template("dashboard.html", user=User.get_user_by_id(user_data), recipes = Recipe.get_all())

@app.route('/recipes/new')
def create_recipe_form():
    return render_template("create_recipe.html")

@app.route('/recipes/new/create', methods=["POST"])
def create_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect("/recipes/new")
    recipe_data = {
        'name' : request.form['name'],
        'description': request.form['description'],
        'instruction': request.form['instruction'],
        'date_made': request.form['date_made'],
        'under_thirty':request.form['under_thirty'],
        'user_id': session['user_id']
    }
    Recipe.create_recipe( recipe_data)
    return redirect('/dashboard')

@app.route("/recipes/<int:id>")
def show_recipe(id):
    user_data = {
        'id' : session["user_id"]
    }
    data = {
        'id' : id
    }
    return render_template("show_recipe.html", recipe = Recipe.get_one(data), user=User.get_user_by_id(user_data))


@app.route("/recipes/<int:id>/edit")
def edit_recipe(id):
    data = {
        'id' : id
    }
    return render_template("edit.html", recipe = Recipe.get_one(data))

@app.route("/recipes/<int:id>/delete")
def delete(id):
    data = {
        'id' :id
    }
    return render_template("delete.html", recipe = Recipe.get_one(data))

@app.route("/recipes/<int:id>/update", methods = ["POST"])
def update(id):
    if not Recipe.validate_recipe(request.form):
        return redirect("/recipes/<int:id>/edit")
    Recipe.update(request.form)
    return redirect("/dashboard")

@app.route("/recipes/<int:id>/destroy", methods = ["POST"])
def destroy(id):
    Recipe.destroy(request.form)
    return redirect("/dashboard")