"""agregar_trigger_search_vector

Revision ID: b9317907eeb8
Revises: 8a5854a8cd30
Create Date: 2026-06-17 18:21:56.224385

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9317907eeb8'
down_revision: Union[str, Sequence[str], None] = '8a5854a8cd30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Ejecutamos el UPDATE masivo para los productos que ya tienen cargados
    op.execute("""
        UPDATE productos 
        SET search_vector = to_tsvector('spanish', COALESCE(titulo, '') || ' ' || COALESCE(descripcion, ''));
    """)
    
    # 2. Creamos el Trigger para que de ahora en más se calcule solo al insertar/actualizar
    op.execute("""
        CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
        ON productos FOR EACH ROW EXECUTE FUNCTION
        tsvector_update_trigger(search_vector, 'pg_catalog.spanish', titulo, descripcion);
    """)


def downgrade() -> None:
    # Si quisieran tirar atrás la migración, borramos el trigger
    op.execute("DROP TRIGGER IF EXISTS tsvectorupdate ON productos;")
