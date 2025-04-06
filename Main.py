from flask import Flask
from src.connection.db_connection import Connection
from src.models.models import Models
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

class Main:
    def __init__(self):
        self.app = Flask(__name__)

        self.connection = Connection()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.connection.connect()  
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
        
        self.db = SQLAlchemy(self.app)
        self.models = Models(self.db)
        self.migrate = Migrate(self.app, self.db)  # Migraciones de la base de datos

    def startApp(self):
        self.app.run(debug=True)

    def getApp(self):
        return self.app

if __name__ == '__main__':
    main = Main()
    main.startApp()
