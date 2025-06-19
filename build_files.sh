#!/bin/bash
echo "BUILD START"
set -e
echo "🔧 Collecting static files..."
python3.9 manage.py collectstatic --noinput --clear
echo "BUILD END"