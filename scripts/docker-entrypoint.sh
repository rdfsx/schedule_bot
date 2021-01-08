#!/bin/sh

set -e

if [ -n "${RUN_MIGRATIONS}" ]; then
  alembic upgrade head
fi

exec python -O -m app