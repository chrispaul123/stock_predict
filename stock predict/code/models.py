from db import db


class ARTICLE(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.Text)
    datetime = db.Column(db.Text)
    url = db.Column(db.Text)
    article = db.Column(db.Text)
    motion = db.Column(db.Float)


class ARTICLE1(db.Model):
    __tablename__ = 'article1'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.Text)
    datetime = db.Column(db.Text)
    url = db.Column(db.Text)
    article = db.Column(db.Text)
    motion = db.Column(db.Float)


class ARTICLE2(db.Model):
    __tablename__ = 'article2'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.Text)
    datetime = db.Column(db.Text)
    url = db.Column(db.Text)
    article = db.Column(db.Text)
    motion = db.Column(db.Float)
