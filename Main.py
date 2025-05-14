from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from src.connection.db_connection import Connection
from src.models.models import Models
from src.config.app_initializer import AppInitializer

class Main:
    def __init__(self):
        self.app = Flask(__name__)

        try:
            self.connection = Connection()
            self.app.config['SQLALCHEMY_DATABASE_URI'] = self.connection.connect()
        except Exception as e:
            print(f" Error al conectar con la base de datos: {e}")

        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.db = SQLAlchemy(self.app)
        self.models = Models(self.db)

        with self.app.app_context():
            try:
                self.db.create_all()
            except Exception as e:
                print(f" Error al crear tablas: {e}")
    
        self.migrate = Migrate(self.app, self.db)
        self.app_initializer = AppInitializer(self.app, self.db, self.models)

        CORS(self.app)

        self.add_ping_route()

    def add_ping_route(self):
        @self.app.route("/ping", methods=["GET"])
        def ping():
            return jsonify({"status": "alive"}), 200

    def startApp(self):
        self.app.run(debug=True, host="0.0.0.0", port=5000)

    def getApp(self):
        return self.app
