class ClienteController:
    def __init__(self,cliente_service):
        """
        Inicializa el controlador de cliente con el servicio proporcionado.
        """
        self.cliente_service=cliente_service