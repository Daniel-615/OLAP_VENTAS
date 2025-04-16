from flask import request
class VendedorRoutes:
    def __init__(self,app,app_initializer):
        """
        Inicializa las rutas de la aplicación con la instancia de Flask proporcionada."""
        self.app=app
        self.app_initializer=app_initializer
        self.routes()
    def routes(self):
        @self.app.route('/ventas/post/vendedor',methods=['POST'])
        def post_vendedor():
            """
            Maneja la solicitud POST para el recurso vendedor.
            """
            data = request.get_json()
            if not data:
                return {"error": "Request body is missing or invalid"}, 400
            return self.app_initializer.getVendedorControllers().post_vendedor(data)
        @self.app.route('/ventas/get/vendedor',methods=['GET'])
        def get_vendedor():
            """
            Maneja la solicitud GET para el recurso vendedor.
            """
            return self.app_initializer.getVendedorControllers().get_vendedor()
        @self.app.route('/ventas/put/vendedor/<uuid:id>',methods=['PUT'])
        def put_vendedor(id):
            """
            Maneja la solicitud PUT para el recurso vendedor.
            """
            data = request.get_json()
            if not data:
                return {"error": "Request body is missing or invalid"}, 400
            return self.app_initializer.getVendedorControllers().put_vendedor(id,data)
        @self.app.route('/ventas/get/vendedor/<uuid:id>',methods=['GET'])
        def get_vendedor_by_id(id):
            """
            Maneja la solicitud GET para el recurso vendedor por id.
            """
            return self.app_initializer.getVendedorControllers().get_vendedor_id(id)
        @self.app.route('/ventas/delete/vendedor/<uuid:id>',methods=['PUT'])
        def delete_vendedor(id):
            """
            Maneja la solicitud PUT para desactivar un vendedor.
            """
            return self.app_initializer.getVendedorControllers().delete_vendedor(id)
        
    