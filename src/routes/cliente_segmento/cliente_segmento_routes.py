from flask import request
class ClienteSegmentoRoutes:
    def __init__(self,app,app_initializer):
        """
        Inicializa las rutas de la aplicación con la instancia de Flask proporcionada."""
        self.app=app
        self.app_initializer=app_initializer
        self.routes()
    def routes(self):
        @self.app.route('/ventas/post/cliente_segmento',methods=['POST'])
        def post_cliente_segmento():
            """
            Maneja la solicitud POST para el recurso cliente_segmento.
            """
            data = request.get_json()
            if not data:
                return {"error": "Request body is missing or invalid"}, 400
            return self.app_initializer.getClienteSegmentoControllers().post_cliente_segmento(data)
        @self.app.route('/ventas/get/cliente_segmento',methods=['GET'])
        def get_cliente_segmento():
            """
            Maneja la solicitud GET para el recurso cliente_segmento.
            """
            return self.app_initializer.getClienteSegmentoControllers().get_cliente_segmento()
        @self.app.route('/ventas/put/cliente_segmento/<uuid:id>',methods=['PUT'])
        def put_cliente_segmento(id):
            """
            Maneja la solicitud PUT para el recurso cliente_segmento.
            """
            data = request.get_json()
            if not data:
                return {"error": "Request body is missing or invalid"}, 400
            return self.app_initializer.getClienteSegmentoControllers().put_cliente_segmento(id,data)
        @self.app.route('/ventas/get/cliente_segmento/<uuid:id>',methods=['GET'])
        def get_cliente_segmento_by_id(id):
            """
            Maneja la solicitud GET para el recurso cliente_segmento por id.
            """
            return self.app_initializer.getClienteSegmentoControllers().get_cliente_segmento_id(id)