from .sql_extensions import db


class Directors(db.Model):
    __tablename__ = "directors"
    id = db.Column(db.Integer, primary_key=True)
    director_name = db.Column(db.String(250), unique=True, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    movies = db.relationship('Shows', backref='shows', lazy=True)


class Shows(db.Model):
    __tablename__ = "shows"
    id = db.Column(db.Integer, primary_key=True)
    show_name = db.Column(db.String(250), unique=True, nullable=False)
    show_type = db.Column(db.Enum('movie', 'episode', 'series'), unique=True, nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'), nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
