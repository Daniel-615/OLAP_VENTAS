from flask import request,jsonify
class TiendaRoutes:
    def __init__(self,app,app_initializer,limiter):
        """
        Inicializa las rutas de la aplicación con la instancia de Flask proporcionada."""
        self.app=app
        self.app_initializer=app_initializer
        self.limiter=limiter
        self.routes()
    def routes(self):
        @self.app.route('/ventas/post/tienda',methods=['POST'])
        @self.limiter.limit("10 per minute")
        def post_tienda():
            """
            Maneja la solicitud POST para el recurso tienda.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getTiendaControllers().post_tienda(data)
        @self.app.route('/ventas/get/tienda',methods=['GET'])
        @self.limiter.limit("10 per minute")
        def get_tienda():
            """
            Maneja la solicitud GET para el recurso tienda.
            """
            return self.app_initializer.getTiendaControllers().get_tienda()
        @self.app.route('/ventas/put/tienda/<uuid:id>',methods=['PUT'])
        @self.limiter.limit("10 per minute")
        def put_tienda(id):
            """
            Maneja la solicitud PUT para el recurso tienda.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getTiendaControllers().put_tienda(id,data)
        @self.app.route('/ventas/get/tienda/<uuid:id>',methods=['GET'])
        @self.limiter.limit("10 per minute")
        def get_tienda_by_id(id):
            """
            Maneja la solicitud GET para el recurso tienda por id.
            """
            return self.app_initializer.getTiendaControllers().get_tienda_id(id)
        