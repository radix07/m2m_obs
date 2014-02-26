import urlparse

#Datbase information for Heroku postgres
#username: leqslquceprcjb
#password: bTO0DubrLXbT7fdVjIf-c-nDvI
#port: 5432
#database: d9rfmhttltdj9c
#host: ec2-54-197-227-238.compute-1.amazonaws.com
#postgres://leqslquceprcjb:bTO0DubrLXbT7fdVjIf-c-nDvI@ec2-54-197-227-238.compute-1.amazonaws.com:5432/d9rfmhttltdj9c

##Postgres
'''

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
'''

