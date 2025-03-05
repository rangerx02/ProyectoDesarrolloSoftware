@echo off
cd "C:\Users\Gfmt\Desktop\Todo\Univalle Gean\6-Univalle Sexto Semestre\Desarrollo de Software\ProyectoDesarrolloSoftware"
git pull origin HEAD
git add .
git commit -m "Actualización automática del trabajo realizado"
git push origin HEAD
echo Actualización completada
