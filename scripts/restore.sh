#!/bin/bash

set -a
source .env
set +a

echo "Backups disponibles:"
echo ""

ls backups

echo ""
read -p "Ingrese el nombre del backup a restaurar: " ARCHIVO

if [ ! -f "backups/$ARCHIVO" ]; then
    echo ""
    echo "El archivo no existe."
    exit 1
fi

echo ""
echo "Restaurando base de datos..."

docker exec -i "$POSTGRES_CONTAINER" \
psql \
-U "$POSTGRES_USER" \
-d "$POSTGRES_DB" \
< "backups/$ARCHIVO"

if [ $? -eq 0 ]; then
    echo ""
    echo "Restauración completada correctamente."
else
    echo ""
    echo "Ocurrió un error durante la restauración."
fi