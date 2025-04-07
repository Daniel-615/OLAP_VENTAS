class GerenteRoutes:
    def __init__(self,app):
        """
        Inicializa las rutas de la aplicación con la instancia de Flask proporcionada."""
        self.app=app
        self.routes()
    def routes(self):
        @self.app.route('/ventas/post/gerente',methods=['POST'])
        def post_gerente():
            """
            Maneja la solicitud POST para el recurso gerente.
            """
            return self.gerente_controller.post_gerente()
        @self.app.route('/ventas/get/gerente',methods=['GET'])
        def get_gerente():
            """
            Maneja la solicitud GET para el recurso gerente.
            """
            return self.gerente_controller.get_gerente()
        @self.app.route('/ventas/put/gerente/<uuid:id>',methods=['PUT'])
        def put_gerente(id):
            """
            Maneja la solicitud PUT para el recurso gerente.
            """
            return self.gerente_controller.put_gerente(id)
        @self.app.route('/ventas/get/gerente/<uuid:id>',methods=['GET'])
        def get_gerente_by_id(id):
            """
            Maneja la solicitud GET para el recurso gerente por id.
            """
            return self.gerente_controller.get_gerente_id(id)
