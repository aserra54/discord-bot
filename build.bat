@echo off

set OUT_DIR=.bot

if exist "%OUT_DIR%" rmdir /s/q "%OUT_DIR%"
mkdir "%OUT_DIR%"

copy .token "%OUT_DIR%"
copy src\*.py "%OUT_DIR%"
copy etc\* "%OUT_DIR%"

python -m venv "%OUT_DIR%\.env"
call "%OUT_DIR%\.env\Scripts\activate.bat"
pip install -r etc\requirements.txt
call "%OUT_DIR%\.env\Scripts\deactivate.bat"

set "RUN_SCRIPT=%OUT_DIR%\run.bat"
echo @echo off> "%RUN_SCRIPT%"
echo call .env\Scripts\activate.bat>> "%RUN_SCRIPT%"
echo python bot.py>> "%RUN_SCRIPT%"
echo call .env\Scripts\deactivate.bat>> "%RUN_SCRIPT%"
