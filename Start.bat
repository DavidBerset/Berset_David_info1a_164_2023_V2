@echo off
echo "Démarrage en cours ..."
echo "Installations des dépendances ..."
pip install -r requirements.txt
echo "importation de la base de données"
python.exe 1_ImportationDumpSql.py
python.exe run_mon_app.py
echo "Fin du programme"
pause