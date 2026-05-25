from sqlalchemy import Column, Integer, String
from app.db.base import Base

@dataclass(init=False, repr=True, eq=True)
class Atributo(db.Model):
    __tablename__ = 'atributos'

    id_atributo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    clave = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Text, nullable=False) 

    # Relación bidireccional
    producto = db.relationship('Producto', back_populates='atributos')