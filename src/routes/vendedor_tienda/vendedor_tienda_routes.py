class VendedorTiendaRoutes:
    def __init__(self,app_initilizer):
        """
        Inicializa las rutas de la aplicación con la instancia de Flask proporcionada."""
        self.app=app_initilizer
        self.routes()
    def routes(self):
        @self.app.route('/ventas/vendedor/tienda/post',methods=['POST'])
        def post_vendedor_tienda():
            """
            Endpoint para registrar un vendedor en una tienda.
            """
            return self.app.vendedor_tienda_controller.post_vendedor_tienda()
        @self.app.route('/ventas/vendedor/tienda/get',methods=['GET'])
        def get_vendedor_tienda():
            """
            Endpoint para obtener la información de un vendedor en una tienda.
            """
            return self.app.vendedor_tienda_controller.get_vendedor_tienda()
        @self.app.route('/ventas/vendedor/tienda/get/<uuid:id_vendedor_tienda>',methods=['GET'])
        def get_vendedor_tienda_by_id(id_vendedor_tienda):
            """
            Endpoint para obtener un vendedor en una tienda por su ID.
            """
            return self.app.vendedor_tienda_controller.get_vendedor_tienda_by_id(id_vendedor_tienda)
        @self.app.route('/ventas/vendedor/tienda/put/<uuid:id_vendedor_tienda>',methods=['PUT'])
        def put_vendedor_tienda(id_vendedor_tienda):
            """
            Endpoint para actualizar un vendedor en una tienda por su ID.
            """
            return self.app.vendedor_tienda_controller.put_vendedor_tienda(id_vendedor_tienda)