#!/bin/bash

echo "🔧 Building static files..."
python3.9 manage.py collectstatic --noinput
