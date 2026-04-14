@echo off
title ORION CLOUD SERVER

cd /d %~dp0

if not exist "venv\Scripts\activate.bat" (
    echo ERRO: Ambiente virtual nao encontrado!
    pause
    exit
)

call venv\Scripts\activate

echo Ambiente ativado.
echo Iniciando servidor...

uvicorn main:app --host 127.0.0.1 --port 8000 --reload

pause