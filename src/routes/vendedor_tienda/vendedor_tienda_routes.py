from flask import request, jsonify

class VendedorTiendaRoutes:
    def __init__(self, app, app_initializer,limiter):
        """
        Inicializa las rutas de la aplicación con la instancia de Flask proporcionada.
        """
        self.app = app
        self.app_initializer = app_initializer
        self.limiter = limiter
        self.routes()

    def routes(self):
        @self.app.route('/ventas/vendedor/tienda/post', methods=['POST'])
        @self.limiter.limit("10 per minute")
        def post_vendedor_tienda():
            """
            Endpoint para registrar un vendedor en una tienda.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getVendedorTiendaControllers().post_vendedor_tienda(data)

        @self.app.route('/ventas/vendedor/tienda/get', methods=['GET'])
        @self.limiter.limit("10 per minute")
        def get_vendedor_tienda():
            """
            Endpoint para obtener la lista de vendedores asignados a tiendas.
            """
            return self.app_initializer.getVendedorTiendaControllers().get_vendedor_tienda()

        @self.app.route('/ventas/vendedor/tienda/get/<uuid:id_vendedor_tienda>', methods=['GET'])
        @self.limiter.limit("10 per minute")
        def get_vendedor_tienda_by_id(id_vendedor_tienda):
            """
            Endpoint para obtener un vendedor en una tienda por su ID.
            """
            return self.app_initializer.getVendedorTiendaControllers().get_vendedor_tienda_id(id_vendedor_tienda)

        @self.app.route('/ventas/vendedor/tienda/put/<uuid:id_vendedor_tienda>', methods=['PUT'])
        @self.limiter.limit("10 per minute")
        def put_vendedor_tienda(id_vendedor_tienda):
            """
            Endpoint para actualizar (dar de baja) una relación vendedor-tienda por su ID.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getVendedorTiendaControllers().put_vendedor_tienda(id_vendedor_tienda, data)
