from flask import request,jsonify
class GerenteRoutes:
    def __init__(self,app,app_initializer,limiter):
        """
        Inicializa las rutas de la aplicación con la instancia de Flask proporcionada."""
        self.app=app
        self.app_initializer=app_initializer
        self.limiter=limiter
        self.routes()
    def routes(self):
        @self.app.route('/ventas/post/gerente',methods=['POST'])
        @self.limiter.limit("10 per minute")
        def post_gerente():
            """
            Maneja la solicitud POST para el recurso gerente.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getGerenteControllers().post_gerente(data)
        @self.app.route('/ventas/get/gerente',methods=['GET'])
        @self.limiter.limit("5 per minute")
        def get_gerente():
            """
            Maneja la solicitud GET para el recurso gerente.
            """
            return self.app_initializer.getGerenteControllers().get_gerente()
        @self.app.route('/ventas/put/gerente/<uuid:id>',methods=['PUT'])
        @self.limiter.limit("10 per minute")
        def put_gerente(id):
            """
            Maneja la solicitud PUT para el recurso gerente.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getGerenteControllers().put_gerente(id,data)
        @self.app.route('/ventas/get/gerente/<uuid:id>',methods=['GET'])
        @self.limiter.limit("5 per minute")
        def get_gerente_by_id(id):
            """
            Maneja la solicitud GET para el recurso gerente por id.
            """
            return self.app_initializer.getGerenteControllers().get_gerente_id(id)
