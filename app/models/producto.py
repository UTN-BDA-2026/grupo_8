from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class Producto(db.Model):
    __tablename__ = 'productos'

    id_producto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    asin = db.Column(db.String(20), unique=True, nullable=False)
    titulo = db.Column(db.String(255), nullable=True)

    # Relaciones bidireccionales
    atributos = db.relationship('Atributo', back_populates='producto', cascade='all, delete-orphan')
    rankings = db.relationship('Ranking', back_populates='producto', cascade='all, delete-orphan')
    relaciones = db.relationship('Relacion', back_populates='producto', cascade='all, delete-orphan')
