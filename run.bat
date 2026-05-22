@echo off

if not exist .venv\ (
	echo === Animal Crossing Map Viewer ===
	echo Press any key to perform first-time virtual environment setup
	pause >nul

	echo Creating virtual environment, this may take a moment
	python -m venv .venv >nul

	echo Activating virtual environment
	call .venv\Scripts\activate.bat

	echo Installing dependencies
	pip install -r requirements.txt >nul
	echo Done!
	echo(
) else (
	call .venv\Scripts\activate.bat
)

python main.py %~dp0 %~dp0assets\
