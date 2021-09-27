import os

DATABASE = os.getenv("PG_DATABASE")
HOSTNAME = os.getenv("PG_HOSTNAME")
PORT = os.getenv("PG_PORT")
USER = os.getenv("PG_USER")
PWD = os.getenv("PG_PWD")
SCHEMA = os.getenv("PG_SCHEMA")