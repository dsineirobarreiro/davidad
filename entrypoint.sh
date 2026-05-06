#!/bin/sh

echo "⏳ Esperando base de datos..."

# espera básica a que Django pueda conectar
while ! python manage.py check --database default; do
  sleep 2
done

echo "📦 Aplicando migraciones..."
python manage.py migrate --noinput

echo "🚀 Iniciando servidor..."
exec "$@"