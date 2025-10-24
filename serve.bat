@echo off
SET PYTHONPYCACHEPREFIX=.\__pycache__\
SET FLASK_APP=app.py
SET FLASK_ENV=development

REM Clean all __pycache__ folders recursively
for /d /r %%G in (__pycache__) do (
	echo Deleting "%%G"
	rd /s /q "%%G"
)

call .\venv\Scripts\activate.bat
cls
nodemon --exec flask run --watch