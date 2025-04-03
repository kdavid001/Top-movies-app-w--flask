import sqlite3
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap5 import Bootstrap  # ✅ Correct import
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired
from markupsafe import Markup
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from db import session, Movies
app = Flask(__name__)
app.config['SECRET_KEY'] = '5fc183cacb94d476269aad5d0133b9f95664f2f5ec197870388679e5c76ab539'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
Bootstrap(app)  # ✅ Correct way to initialize Bootstrap
# Create database instance
db = SQLAlchemy()
db.init_app(app)

year_choices = [(str(y), str(y)) for y in range(1900, datetime.now().year + 1)]

# -------- For the Movie API ---------- #
import requests
url ="https://api.themoviedb.org/3/search/movie"
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwMWJhZGIxN2NmNjFkY2Q2MzhkYjZkYWEzNjQ3ODkxYiIsIm5iZiI6MTc0MzQyNzM5NC41OTYsInN1YiI6IjY3ZWE5NzQyNTA0MGE3NWI0YWU1N2QwMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.IISVbxUhTOnUZOQdzb6RqTiyUDUH-59IKVovs62TgYU"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwMWJhZGIxN2NmNjFkY2Q2MzhkYjZkYWEzNjQ3ODkxYiIsIm5iZiI6MTc0MzQyNzM5NC41OTYsInN1YiI6IjY3ZWE5NzQyNTA0MGE3NWI0YWU1N2QwMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.IISVbxUhTOnUZOQdzb6RqTiyUDUH-59IKVovs62TgYU"
}





# class Movies(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(250), nullable=False)
#     year = db.Column(db.Integer, nullable=False)
#     description = db.Column(db.String(500), nullable=False)
#     rating = db.Column(db.Float, nullable=False)
#     ranking = db.Column(db.Integer, nullable=False)
#     review = db.Column(db.String(500), nullable=False)
#     img_url = db.Column(db.String(500), nullable=False)


# Create table if not exists
with app.app_context():
    db.create_all()


## Add form
class MovieForms(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    year = SelectField("Year", choices=year_choices, validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    rating = FloatField('Rating /10', validators=[DataRequired()])
    ranking = IntegerField('Ranking', validators=[DataRequired()])
    review = StringField('Review', validators=[DataRequired()])
    img_url = StringField('IMG', validators=[DataRequired()])
    submit = SubmitField('Submit')


# class RateMovieForm(FlaskForm):
#     rating = StringField("Your Rating Out of 10 e.g. 7.5")
#     review = StringField("Your Review")
#     submit = SubmitField("Done")

class FindMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


@app.route("/")
def home():
    movies = session.query(Movies).all()
    return render_template("index.html", movies=movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = MovieForms()
    if form.validate_on_submit():
        new_movie = Movies(
            title=form.title.data,
            # year=form.year.data,
            # description=form.description.data,
            # rating=form.rating.data,
            # ranking=form.ranking.data,
            # review=form.review.data,
            # img_url=form.img_url.data
        )
        response = requests.get(url)
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('home'))  # Redirect to home page after adding
    return render_template('add.html', form=form)


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = FindMovieForm()
    if form.validate_on_submit():
        movie_name = form.title.data

        return redirect(url_for('select'), movie=movie_name)
    return render_template("add.html", form=form)

@app.route("/select", methods=["GET", "POST"])
def select():

    return render_template("select.html")

@app.route("/update/<int:movie_id>", methods=["GET", "POST"])
def update(movie_id):
    movie = session.query(Movies).filter_by(id=movie_id).first()
    if not movie:
        return "Movie not found", 404

    form = MovieForms(obj=movie)

    if form.validate_on_submit():
        movie.rating = form.rating.data
        movie.review = form.review.data
        session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", form=form, movie=movie)


@app.route("/delete/<int:movie_id>", methods=["GET", "POST"])
def delete(movie_id):
    movie_to_delete = session.query(Movies).filter_by(id=movie_id).first()
    if movie_to_delete:
        session.delete(movie_to_delete)
        session.commit()
        return redirect(url_for("home"))
    return "Movie not found", 404


if __name__ == '__main__':
    app.run(debug=True)