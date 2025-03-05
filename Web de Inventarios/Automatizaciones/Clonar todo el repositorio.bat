@echo off
set REPO_URL=https://github.com/rangerx02/ProyectoDesarrolloSoftware.git
set REPO_DIR="C:\Users\Gfmt\Desktop\Todo\Univalle Gean\6-Univalle Sexto Semestre\Desarrollo de Software\ProyectoDesarrolloSoftware"

:: Verificar si el repositorio ya existe
if not exist %REPO_DIR% (
    echo Clonando el repositorio...
    git clone %REPO_URL% %REPO_DIR%
    echo Clonación completada
) else (
    echo El repositorio ya existe. No se necesita clonar.
)

