web: newrelic-admin run-program gunicorn runp-heroku:app --timeout 40
init: python db_create.py 
upgrade: python db_upgrade.py
etheriosUpdate: python updateFromCloud.py --timeout 240
initF: python manager.py db init
revF: python manager.py db revision
migrateF: python manager.py db migrate
upgradeF: python manager.py db upgrade
etheriosUpdateTO: gunicorn updateFromCloud:app --timeout 120
etheriosUpdateNR: newrelic-admin run-program updateFromCloud:app run_gunicorn --timeout 120