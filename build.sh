#!/usr/bin/env bash
# build.sh - Render deployment build script
set -o errexit

echo "🚀 Installing dependencies..."
pip install -r requirements.txt

echo "📦 Collecting static files..."
python manage.py collectstatic --no-input

echo "🗄️  Running database migrations..."
python manage.py migrate

echo "✅ Build completed successfully!"
