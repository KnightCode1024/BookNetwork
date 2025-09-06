set -e
echo "Waiting for postgres..."
sleep 3
cd src
echo "Applying Alembic migrations..."
uv run alembic upgrade head
echo "Migrations applied"
sleep 3
echo "Starting application..."
uv run python3 main.py
