class ClienteSegmentoRoutes:
    def __init__(self,app_initilizer):
        """
        Inicializa las rutas de la aplicación con la instancia de Flask proporcionada."""
        self.app=app_initilizer
        self.routes()
    def routes(self):
        @self.app.route('/post/cliente_segmento',methods=['POST'])
        def post_cliente_segmento():
            """
            Maneja la solicitud POST para el recurso cliente_segmento.
            """
            return self.cliente_segmento_controller.post_cliente_segmento()
        @self.app.route('/get/cliente_segmento',methods=['GET'])
        def get_cliente_segmento():
            """
            Maneja la solicitud GET para el recurso cliente_segmento.
            """
            return self.cliente_segmento_controller.get_cliente_segmento()
        @self.app.route('/put/cliente_segmento/<uuid:id>',methods=['PUT'])
        def put_cliente_segmento(id):
            """
            Maneja la solicitud PUT para el recurso cliente_segmento.
            """
            return self.cliente_segmento_controller.put_cliente_segmento(id)
        @self.app.route('/get/cliente_segmento/<uuid:id>',methods=['GET'])
        def get_cliente_segmento_by_id(id):
            """
            Maneja la solicitud GET para el recurso cliente_segmento por id.
            """
            return self.cliente_segmento_controller.get_cliente_segmento_id(id)