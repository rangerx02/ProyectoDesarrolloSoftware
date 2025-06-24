@echo off
cd "C:\Users\Gfmt\Desktop\Desarrollo de software\ProyectoDesarrolloSoftware"  
git pull origin HEAD
git add .
git commit -m "Actualización automática"
git push origin HEAD
echo Actualización completada
