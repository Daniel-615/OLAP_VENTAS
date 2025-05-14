from flask import request, jsonify

class CheckServer:
    def __init__(self, app, app_initializer):
        self.app = app
        self.app_initializer = app_initializer
        self.routes()

    def routes(self):
        @self.app.route('/ping', methods=['GET'])
        def ping():
            return jsonify({'message': 'Backend activo'}), 200
