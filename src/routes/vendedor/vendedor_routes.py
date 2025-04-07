class VendedorRoutes:
    def __init__(self,app_initilizer):
        """
        Inicializa las rutas de la aplicación con la instancia de Flask proporcionada."""
        self.app=app_initilizer
        self.routes()
    def routes(self):
        @self.app.route('/ventas/post/vendedor',methods=['POST'])
        def post_vendedor():
            """
            Maneja la solicitud POST para el recurso vendedor.
            """
            return self.vendedor_controller.post_vendedor()
        @self.app.route('/ventas/get/vendedor',methods=['GET'])
        def get_vendedor():
            """
            Maneja la solicitud GET para el recurso vendedor.
            """
            return self.vendedor_controller.get_vendedor()
        @self.app.route('/ventas/put/vendedor/<uuid:id>',methods=['PUT'])
        def put_vendedor(id):
            """
            Maneja la solicitud PUT para el recurso vendedor.
            """
            return self.vendedor_controller.put_vendedor(id)
        @self.app.route('/ventas/get/vendedor/<uuid:id>',methods=['GET'])
        def get_vendedor_by_id(id):
            """
            Maneja la solicitud GET para el recurso vendedor por id.
            """
            return self.vendedor_controller.get_vendedor_id(id)