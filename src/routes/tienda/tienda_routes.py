class TiendaRoutes:
    def __init__(self,app_initilizer):
        """
        Inicializa las rutas de la aplicación con la instancia de Flask proporcionada."""
        self.app=app_initilizer
        self.routes()
    def routes(self):
        @self.app.route('/ventas/post/tienda',methods=['POST'])
        def post_tienda():
            """
            Maneja la solicitud POST para el recurso tienda.
            """
            return self.tienda_controller.post_tienda()
        @self.app.route('/ventas/get/tienda',methods=['GET'])
        def get_tienda():
            """
            Maneja la solicitud GET para el recurso tienda.
            """
            return self.tienda_controller.get_tienda()
        @self.app.route('/ventas/put/tienda/<uuid:id>',methods=['PUT'])
        def put_tienda(id):
            """
            Maneja la solicitud PUT para el recurso tienda.
            """
            return self.tienda_controller.put_tienda(id)
        @self.app.route('/ventas/get/tienda/<uuid:id>',methods=['GET'])
        def get_tienda_by_id(id):
            """
            Maneja la solicitud GET para el recurso tienda por id.
            """
            return self.tienda_controller.get_tienda_id(id)
        