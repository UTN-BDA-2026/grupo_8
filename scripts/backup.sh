#!/bin/bash

# Cargar variables del .env
set -e 

set -a
source .env
set +a

mkdir -p backups

# En vez de solamente crear el archivo con fecha, 
# también genera automáticamente un enlace al último backup.

FECHA=$(date +%Y%m%d_%H%M%S)

ARCHIVO="backups/backup_${FECHA}.sql"

docker exec "$POSTGRES_CONTAINER" \
pg_dump \
-U "$POSTGRES_USER" \
-d "$POSTGRES_DB" \
> "$ARCHIVO"



if [ $? -eq 0 ]; then

    cp "$ARCHIVO" backups/ultimo_backup.sql

    echo ""
    echo "Backup realizado correctamente."
    echo "Archivo generado:"
    echo "$ARCHIVO"

else

    echo "Error al generar el backup."

fi