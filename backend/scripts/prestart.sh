#! /usr/bin/env bash

set -e
set -x

# Let the DB start
python app/core/database/database.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python app/core/database/db_setup.py
