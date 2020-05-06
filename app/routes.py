from flask import render_template, flash, redirect, url_for

from app import app
from app.forms import LoginForm

@app.route("/", methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit() and form.password.data == app.password:
        flash('Logged in')
        return redirect(url_for('game'))
    flash('test')
    return render_template("home.html", form=form)

@app.route("/game")
def game():
    return render_template("game.html")
