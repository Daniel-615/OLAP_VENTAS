from psycopg2 import OperationalError
import os
from dotenv import load_dotenv
load_dotenv(override=True)
class Connection:
    def __init__(self):
        self.host = os.environ.get('DB_HOST')
        self.user = os.environ.get('DB_USER')
        self.password = os.environ.get('DB_PASSWORD')
        self.database = os.environ.get('DB_NAME')
        self.port=os.environ.get('DB_PORT')

    def getHost(self):
        return self.host
    def getUser(self):
        return self.user
    def getPassword(self):
        return self.password
    def getDatabase(self):
        return self.database
    def getPort(self):
        return self.port
    def connect(self):
        try:
            return f"postgresql://{self.getUser()}:{self.getPassword()}@{self.getHost()}:{self.getPort()}/{self.getDatabase()}"
        except OperationalError as e:
            print(f"Error al parsear la ruta: {e}")
