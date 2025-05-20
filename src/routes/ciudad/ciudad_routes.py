from flask import request,jsonify
class CiudadRoutes:
    """
    This class defines the routes for the Ciudad resource.
    """
    def __init__(self,app,app_initializer):
        self.app=app
        self.app_initializer=app_initializer
        self.routes()
    
    def routes(self):
        """
        This method defines the routes for the ciudad resource.
        """
        @self.app.route('/ventas/post/ciudad',methods=['POST'])
        def post_ciudad():
            """
            This method handles the POST request for the ciudad resource.
            """

            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getCiudadControllers().post_ciudad(data)

        @self.app.route('/ventas/get/ciudad',methods=['GET'])
        def get_ciudad():
            """
            This method handles the GET request for the ciudad resource.
            """
            return self.app_initializer.getCiudadControllers().get_ciudad()
        @self.app.route('/ventas/put/ciudad/<uuid:id>',methods=['PUT'])
        def put_ciudad(id):
            """
            This method handles the PUT request for the ciudad resource.
            """
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is missing or invalid"}), 400
            return self.app_initializer.getCiudadControllers().put_ciudad(id,data)
        @self.app.route('/ventas/get/ciudad/<uuid:id>',methods=['GET'])
        def get_ciudad_by_id(id):
            """
            This method handles the GET request for the ciudad resource by id.
            """
            return self.app_initializer.getCiudadControllers().get_ciudad_id(id)

