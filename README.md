Flask framework hosted on Heroku
git init (new)
heroku login
git remote add heroku git@heroku.com:pgsicom.git
git remote add origin https://github.com/radix07/pgsicom.git
(git remote -v) -test remotes
git add *
git commit -m ""
git push heroku master (-f)
heroku open


Deployment Seq:
git add *
git commit -m ""
git push
git push heroku master

Heroku Actions
heroku run init
heroku run upgrade
heroku logs -t (tail track)
heroku logs -n 1000

heroku pg:info -a pgsicom