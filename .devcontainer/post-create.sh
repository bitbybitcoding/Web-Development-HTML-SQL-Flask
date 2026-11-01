#!/usr/bin/env bash
# Runs once when the codespace is created.
set -euo pipefail

echo "==> Installing SQLite command-line tools"
sudo apt-get update -y
sudo apt-get install -y --no-install-recommends sqlite3

echo "==> Installing Python packages"
pip3 install --user --upgrade pip
pip3 install --user -r requirements.txt

echo "==> Making the sqlite3 shell easier to read"
cp .devcontainer/sqliterc "$HOME/.sqliterc"

echo "==> Checking the starter database"
if [ ! -f school.db ]; then
  python3 tools/make_school_db.py
fi

echo
echo "Ready!  Python $(python3 --version | cut -d' ' -f2), Flask $(python3 -c 'import importlib.metadata as m; print(m.version("flask"))'), SQLite $(sqlite3 --version | cut -d' ' -f1)"
