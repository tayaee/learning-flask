@echo off
python -c "import secrets; print(f'SECRET_KEY = \"{secrets.token_hex()}\"');"