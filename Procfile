web: gunicorn runp-heroku:app --timeout 600
init: python db_create.py 
upgrade: python db_upgrade.py
etherioUpdate: python updateFromCloud.py