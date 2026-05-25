from dataclasses import dataclass
from app import db

@dataclass(init=False, repr=True, eq=True)
class Relacion(db.Model):
    __tablename__ = 'relaciones'

    id_relacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    asin_relacionado = db.Column(db.String(20), nullable=False)
    tipo_relacion = db.Column(db.String(20), nullable=False)

    # Relación bidireccional
    producto = db.relationship('Producto', back_populates='relaciones')