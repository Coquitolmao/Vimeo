#!/bin/sh
. ./set_env_secrets.sh
exec uvicorn main:app --host 0.0.0.0 --port 8000

