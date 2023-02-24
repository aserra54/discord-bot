@REM @echo off

if exist .bot rmdir /s/q .bot
mkdir .bot

copy requirements.txt .bot
python -m venv .bot\.env
call .bot\.env\Scripts\activate.bat
pip install -r requirements.txt

copy *.py .bot
copy .token .bot
copy rules.json .bot

python bot.py
