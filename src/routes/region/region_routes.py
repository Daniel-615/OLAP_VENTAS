class RegionRoutes:
    def __init__(self,app_initilizer):
        """
        Inicializa las rutas de la aplicación con la instancia de Flask proporcionada."""
        self.app=app_initilizer
        self.routes()
    def routes(self):
        """
        Define las rutas de la aplicación."""
        @self.app.route('/ventas/post/region',methods=['POST'])
        def post_region():
            """
            Maneja la solicitud POST para el recurso region.
            """
            return self.region_controller.post_region()
        @self.app.route('/ventas/get/region',methods=['GET'])
        def get_region():
            """
            Maneja la solicitud GET para el recurso region.
            """
            return self.region_controller.get_region()
        @self.app.route('/ventas/put/region/<uuid:id>',methods=['PUT'])
        def put_region(id):
            """
            Maneja la solicitud PUT para el recurso region.
            """
            return self.region_controller.put_region(id)
        @self.app.route('/ventas/get/region/<uuid:id>',methods=['GET'])
        def get_region_by_id(id):
            """
            Maneja la solicitud GET para el recurso region por id.
            """
            return self.region_controller.get_region_id(id)