from flask import request,jsonify
class ClienteRoutes:
    def __init__(self,app,app_initializer):
        self.app=app
        self.app_initializer=app_initializer
        self.routes()
    def routes(self):
        """
        This method defines the routes for the cliente resource.
        """
        @self.app.route('/ventas/post/cliente',methods=['POST'])
        def post_cliente():
            """
            This method handles the POST request for the cliente resource.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getClienteControllers().post_cliente(data)
        @self.app.route('/ventas/get/cliente',methods=['GET'])
        def get_cliente():
            """
            This method handles the GET request for the cliente resource.
            """
            return self.app_initializer.getClienteControllers().get_cliente()
        @self.app.route('/ventas/put/cliente/<uuid:id>',methods=['PUT'])
        def put_cliente(id):
            """
            This method handles the PUT request for the cliente resource.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getClienteControllers().put_cliente(id,data)
        @self.app.route('/ventas/get/cliente/<uuid:id>',methods=['GET'])
        def get_cliente_by_id(id):
            """
            This method handles the GET request for the cliente resource by id.
            """
            return self.app_initializer.getClienteControllers().get_cliente_id(id)
        