# tests/test_categoria_repo.py
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.repositories.categoria_repository import categoria_repo
from app.models import Categoria

def crear_datos_de_prueba(db: Session):
    """Inserta categorías de prueba usando text() para SQLAlchemy 2.0."""
    db.execute(
        text("INSERT INTO categorias (id_categoria, nombre) VALUES (1, 'Tecnologia') ON CONFLICT DO NOTHING;")
    )
    db.execute(
        text("INSERT INTO categorias (id_categoria, nombre) VALUES (2, 'Hogar') ON CONFLICT DO NOTHING;")
    )
    db.commit()

def test_get_by_name_encuentra_coincidencia_exacta(db_session: Session):
    # Arrange (Preparar los datos en la DB temporal)
    crear_datos_de_prueba(db_session)
    
    # Act (Ejecutar el método del repositorio)
    categoria = categoria_repo.get_by_name(db_session, "Tecnologia")
    
    # Assert (Verificar que devolvió la categoría correcta)
    assert categoria is not None
    assert categoria.id_categoria == 1
    assert categoria.nombre == "Tecnologia"

def test_get_by_name_es_insensible_a_mayusculas_y_minusculas(db_session: Session):
    # Arrange
    crear_datos_de_prueba(db_session)
    
    # Act (Buscamos con una mezcla de mayúsculas y minúsculas "tEcNoLoGíA")
    categoria = categoria_repo.get_by_name(db_session, "tEcNoLoGiA")
    
    # Assert (Debería encontrarla igual gracias al .ilike())
    assert categoria is not None
    assert categoria.id_categoria == 1

def test_get_by_name_devuelve_none_si_no_existe(db_session: Session):
    # Arrange
    crear_datos_de_prueba(db_session)
    
    # Act (Buscamos algo que sabemos que no está)
    categoria = categoria_repo.get_by_name(db_session, "Inexistente")
    
    # Assert
    assert categoria is None