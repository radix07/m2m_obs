web: newrelic-admin run-program gunicorn runp-heroku:app --timeout 40

init: python manager.py db init
rev: python manager.py db revision
migrate: python manager.py db migrate
upgrade: python manager.py db upgrade

etheriosUpdate: python updateFromCloud.py --timeout 240
etheriosUpdateTO: gunicorn updateFromCloud:app --timeout 120
etheriosUpdateNR: newrelic-admin run-program updateFromCloud:app run_gunicorn --timeout 120