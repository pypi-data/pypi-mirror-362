$ErrorActionPreference = "Stop"

ruff check 
pytest 
mypy .\uffutils --follow-untyped-imports