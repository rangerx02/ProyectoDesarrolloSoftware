@echo off
REM Crear entorno virtual
python -m venv my_StockNova

REM Activar entorno virtual
call my_StockNova\Scripts\activate

REM Actualizar pip
python -m pip install --upgrade pip

REM Instalar requerimientos
pip install -r requirements.txt

echo -------------------------------------
echo Entorno virtual creado e instalado.
echo Activa el entorno con:
echo call my_StockNova\Scripts\activate
echo -------------------------------------
pause
