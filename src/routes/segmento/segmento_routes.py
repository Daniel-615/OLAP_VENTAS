from flask import request, jsonify

class SegmentoRoutes:
    def __init__(self, app, app_initializer,limiter):
        """
        Clase que inicializa las rutas para el segmento.
        """
        self.app = app
        self.app_initializer = app_initializer
        self.limiter=limiter
        self.routes()

    def routes(self):
        """
        Define las rutas de la aplicación.
        """
        @self.app.route('/ventas/post/segmento', methods=['POST'])
        @self.limiter.limit("10 per minute")
        def post_segmento():
            """
            Maneja la solicitud POST para el recurso segmento.
            """
            data = request.get_json()
            if not data:
                return jsonify({
                    "error": "Request body is missing or invalid"
                }), 400
            return self.app_initializer.getSegmentoControllers().post_segmento(data)

        @self.app.route('/ventas/get/segmento', methods=['GET'])
        @self.limiter.limit("10 per minute")
        def get_segmentos():
            """
            Maneja la solicitud GET para obtener todos los segmentos.
            """
            return self.app_initializer.getSegmentoControllers().get_segmento() 

        @self.app.route('/ventas/put/segmento/<uuid:id>', methods=['PUT'])
        @self.limiter.limit("10 per minute")
        def put_segmento(id):
            """
            Maneja la solicitud PUT para actualizar un segmento por ID.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getSegmentoControllers().put_segmento(id, data)

        @self.app.route('/ventas/get/segmento/<uuid:id>', methods=['GET'])
        @self.limiter.limit("10 per minute")
        def get_segmento_by_id(id):
            """
            Maneja la solicitud GET para obtener un segmento por ID.
            """
            return self.app_initializer.getSegmentoControllers().get_segmento_id(id)
