import os
import dotenv

dotenv.load_dotenv()

PGSQL_PORT = int(os.getenv("PGSQL_PORT"))
PGSQL_PW = os.getenv("PGSQL_PW")
HOST = os.getenv("HOST")
PGSQL_USER = os.getenv("PGSQL_USER")


# add yaml config here