#!/usr/bin/env bash
set -e

python3 -m utils.wait_for_es
python3 -m utils.wait_for_redis
pytest ./src