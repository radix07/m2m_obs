import os
import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse("ec2-174-129-218-200.compute-1.amazonaws.com")

conn = psycopg2.connect(
    database="d5g2gpc0dpha35",
    user="ynnnmoibdtcimj",
    password="3cNzOVrB0zx-XSAekj7ANrkYZ_",
    host="ec2-174-129-218-200.compute-1.amazonaws.com",
    port=5432
)

