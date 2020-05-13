import csv
from typing import Iterable
from sqlalchemy.exc import IntegrityError
from .db import db


class StateModel(db.Model):
    __tablename__ = 'states'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(),
        onupdate=db.func.now())

    def __repr__(self):
        return '<StateModel {}:"{}">'.format(self.code, self.name)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_code(cls, code):
        return cls.query.filter_by(code=code).first()

    @classmethod
    def import_csv(cls, iterable: Iterable[str]):
        iterable = csv.reader(iterable, delimiter=';')
        header = next(iterable)
        if header != ['codigo', 'nombre']:
            raise ValueError("wrong csv format")
        for code, name in iterable:
            try:
                state = cls(code=code, name=name)
                state.save()
            except IntegrityError:
                db.session.rollback()
                state = cls.get_by_code(code)
                state.name = name
                state.save()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_data(self):
        return dict(id=self.code, name=self.name,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat())


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False, default=0)

    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    state = db.relationship('StateModel', backref=db.backref('users', lazy=True))

    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(),
        onupdate=db.func.now())

    def __repr__(self):
        return '<UserMOdel "{}">'.format(self.name)

    @classmethod
    def get_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_data(self):
        return dict(id=self.id, name=self.name, age=self.age,
            state_id=self.state.code,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat())