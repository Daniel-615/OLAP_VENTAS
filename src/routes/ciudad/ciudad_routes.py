from flask import request

class CiudadRoutes:
    """
    This class defines the routes for the Ciudad resource.
    """
    def __init__(self,app_initilizer):
        self.app=app_initilizer
        self.routes()
    
    def routes(self):
        """
        This method defines the routes for the ciudad resource.
        """
        @self.app.route('/post/ciudad',methods=['POST'])
        def post_ciudad():
            """
            This method handles the POST request for the ciudad resource.
            """

            data = request.get_json()
            if not data:
                return {"error": "Request body is missing or invalid"}, 400
            return self.ciudad_controller.post_ciudad(data)
        @self.app.route('/get/ciudad',methods=['GET'])
        def get_ciudad():
            """
            This method handles the GET request for the ciudad resource.
            """
            return self.ciudad_controller.get_ciudad()
        @self.app.route('/put/ciudad/<uuid:id>',methods=['PUT'])
        def put_ciudad(id):
            """
            This method handles the PUT request for the ciudad resource.
            """
            return self.ciudad_controller.put_ciudad(id)
        @self.app.route('/get/ciudad/<uuid:id>',methods=['GET'])
        def get_ciudad_by_id(id):
            """
            This method handles the GET request for the ciudad resource by id.
            """
            return self.ciudad_controller.get_ciudad_id(id)

