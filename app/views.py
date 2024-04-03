from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from . import app, db, UPLOAD_FOLDER
from .forms import ReviewForm, MovieForm, RegistrationForm, LoginForm
from .models import Review, Movie, User


@app.route('/')
def index():
    movies = Movie.query.order_by(Movie.id.desc()).all()
    return render_template('index.html',
                           movies=movies)


@app.route('/movie/<int:id>', methods=['GET', 'POST'])
def movie(id):
    movie = Movie.query.get(id)
    if movie.reviews:
        avg_score = round(sum(review.score for review in movie.reviews) / len(movie.reviews), 2)
    else:
        avg_score = 0
    form = ReviewForm(score=10)
    if form.validate_on_submit():
        review = Review()
        review.name = form.name.data
        review.text = form.text.data
        review.score = form.score.data
        review.movie_id = movie.id
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('movie', id=movie.id))
    return render_template('movie.html',
                           movie=movie,
                           avg_score=avg_score,
                           form=form)


@app.route('/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    form = MovieForm()
    if form.validate_on_submit():
        movie = Movie()
        movie.title = form.title.data
        movie.description = form.description.data
        image = form.image.data
        image_name = secure_filename(image.filename)
        UPLOAD_FOLDER.mkdir(exist_ok=True)
        movie.image = image_name
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('movie', id=movie.id))
    return render_template('add_movie.html',
                           form=form)


@app.route('/reviews')
@login_required
def reviews():
    reviews = Review.query.order_by(Review.created_date.desc()).all()
    return render_template('reviews.html',
                           reviews=reviews)


@app.route('/delete_review/<int:id>')
@login_required
def delete_review(id):
    review = Review.query.get(id)
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('reviews'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Вход выполнен!', 'alert-success')
            return redirect(url_for('index'))
        else:
            flash('Вход не выполнен!', 'alert-danger')
    return render_template('login.html', form=form)


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно!', 'alert-success')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))