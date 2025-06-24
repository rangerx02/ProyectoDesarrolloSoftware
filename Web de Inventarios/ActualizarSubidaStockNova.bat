@echo off
REM Ruta a tu carpeta raíz del proyecto (ajústala si es necesario)
cd "C:\Users\Gfmt\Desktop\Desarrollo de software\ProyectoDesarrolloSoftware" 

echo ================================
echo 📥 Actualizando repositorio Git...
echo ================================
git pull origin HEAD
git add .
git commit -m "Actualización automática"
git push origin HEAD

echo.
echo =======================================
echo 🐍 Verificando entorno virtual...
echo =======================================

IF NOT EXIST "my_StockNova" (
    echo ➕ Entorno virtual no encontrado. Creando...
    python -m venv my_StockNova
) ELSE (
    echo ✅ Entorno virtual ya existe.
)

echo.
echo =======================================
echo 🚀 Activando entorno e instalando pip...
echo =======================================
call my_StockNova\Scripts\activate

REM Asegura que pip esté actualizado
python -m pip install --upgrade pip

REM Instala dependencias del proyecto
IF EXIST "requirements.txt" (
    pip install -r requirements.txt
    echo ✅ Requerimientos instalados.
) ELSE (
    echo ⚠️ No se encontró el archivo requirements.txt
)

echo.
echo ========================================
echo ✅ Listo. El entorno está configurado.
echo Usa: call my_StockNova\Scripts\activate
echo para comenzar a trabajar.
echo ========================================
pause
