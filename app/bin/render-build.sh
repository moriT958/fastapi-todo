#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# If you're using a Free instance type, you need to
# perform database migrations in the build command.
# Uncomment the following line:

alembic upgrade head