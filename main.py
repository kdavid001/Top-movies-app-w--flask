import sqlite3
import os
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap5 import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
from markupsafe import Markup
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from db import session, Movies

app = Flask(__name__)
app.config['SECRET_KEY'] = 'REMOVED'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
Bootstrap(app)

# database instance
db = SQLAlchemy()
db.init_app(app)
csrf = CSRFProtect(app)
load_dotenv()
year_choices = [(str(y), str(y)) for y in range(1900, datetime.now().year + 1)]

# -------- For the Movie API ---------- #
import requests

url = "https://api.themoviedb.org/3/search/movie"
Image_api_url = "https://image.tmdb.org/t/p/w500"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {os.getenv('API_KEY')}",
}

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


class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5")
    review = StringField("Your Review")


class FindMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


@app.route("/")
def home():
    result = db.session.execute(db.select(Movies).order_by(Movies.rating))
    all_movies = result.scalars().all()  # convert ScalarResult to Python List

    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()

    return render_template("index.html", movies=all_movies)
@app.route("/add", methods=["GET", "POST"])
def add():
    form = FindMovieForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        query_param = {
            "query": f"{movie_title}"
        }
        response = requests.get(url, headers=headers, params=query_param).json()
        data = response["results"]
        return render_template("select.html", options=data)
    return render_template("add.html", form=form)


@app.route("/update/<int:movie_id>", methods=["GET", "POST"])
def update(movie_id):
    movie = db.session.query(Movies).get_or_404(movie_id)
    if not movie:
        return "Movie not found", 404

    form = RateMovieForm(obj=movie)

    if form.validate_on_submit():
        movie.rating = form.rating.data
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", form=form, movie=movie)


@app.route("/delete/<int:movie_id>", methods=["GET", "POST"])
def delete(movie_id):
    # Retrieve the movie object using the passed movie_id
    movie = db.session.query(Movies).get_or_404(movie_id)

    # Delete the movie object
    db.session.delete(movie)
    db.session.commit()

    # Redirect to the home page after deletion
    return redirect(url_for("home"))
@app.route("/edit", methods=["GET", "POST"])
def rate_movie():
    form = RateMovieForm()
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movies, movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)


@app.route("/find")
def find_movie():
    movie_id = request.args.get("id")
    if movie_id:
        movie_api_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        response = requests.get(movie_api_url, headers=headers, params={
            "api_key": os.getenv("API_KEY"), "language": "en-US"})
        print(response)
        data = response.json()
        new_movie = Movies(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            img_url=f"{Image_api_url}{data['poster_path']}",
            description=data["overview"],
            rating=0,
            ranking = 0,
            review= "None",

        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("rate_movie", id=new_movie.id))
    else:
        return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
