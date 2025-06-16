from flask import request,jsonify
class RegionRoutes:
    def __init__(self,app,app_initializer,limiter):
        """
        Inicializa las rutas de la aplicación con la instancia de Flask proporcionada."""
        self.app=app
        self.app_initializer=app_initializer
        self.limiter=limiter
        self.routes()
    def routes(self):
        """
        Define las rutas de la aplicación."""
        @self.app.route('/ventas/post/region',methods=['POST'])
        @self.limiter.limit("10 per minute")
        def post_region():
            """
            Maneja la solicitud POST para el recurso region.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getRegionControllers().post_region(data)
        @self.app.route('/ventas/get/region',methods=['GET'])
        @self.limiter.limit("10 per minute")
        def get_region():
            """
            Maneja la solicitud GET para el recurso region.
            """
            return self.app_initializer.getRegionControllers().get_region()
        @self.app.route('/ventas/put/region/<uuid:id>',methods=['PUT'])
        @self.limiter.limit("10 per minute")
        def put_region(id):
            """
            Maneja la solicitud PUT para el recurso region.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getRegionControllers().put_region(id,data)
        @self.app.route('/ventas/get/region/<uuid:id>',methods=['GET'])
        @self.limiter.limit("10 per minute")
        def get_region_by_id(id):
            """
            Maneja la solicitud GET para el recurso region por id.
            """
            return self.app_initializer.getRegionControllers().get_region_id(id)