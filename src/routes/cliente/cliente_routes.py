class ClienteRoutes:
    def __init__(self,app_initilizer):

        self.app=app_initilizer
        self.routes()
    def routes(self):
        """
        This method defines the routes for the cliente resource.
        """
        @self.app.route('/post/cliente',methods=['POST'])
        def post_cliente():
            """
            This method handles the POST request for the cliente resource.
            """
            return self.cliente_controller.post_cliente()
        @self.app.route('/get/cliente',methods=['GET'])
        def get_cliente():
            """
            This method handles the GET request for the cliente resource.
            """
            return self.cliente_controller.get_cliente()
        @self.app.route('/put/cliente/<int:id>',methods=['PUT'])
        def put_cliente(id):
            """
            This method handles the PUT request for the cliente resource.
            """
            return self.cliente_controller.put_cliente(id)
        @self.app.route('/get/cliente/<int:id>',methods=['GET'])
        def get_cliente_by_id(id):
            """
            This method handles the GET request for the cliente resource by id.
            """
            return self.cliente_controller.get_cliente_id(id)
        