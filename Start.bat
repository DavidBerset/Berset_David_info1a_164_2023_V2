@echo off
echo "Démarrage en cours ..."
echo "Installations des dépendances ..."
pip install -r requirements.txt
python.exe run_mon_app.py
echo "Fin du programme"
pause