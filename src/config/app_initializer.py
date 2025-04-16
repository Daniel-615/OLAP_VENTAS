from src.routes.ciudad.ciudad_routes import CiudadRoutes as CI_R
from src.routes.cliente.cliente_routes import ClienteRoutes as C_R
from src.routes.cliente_segmento.cliente_segmento_routes import ClienteSegmentoRoutes as C_S_R
from src.routes.gerente.gerente_routes import GerenteRoutes as G_R
from src.routes.region.region_routes import RegionRoutes as R_R
from src.routes.vendedor.vendedor_routes import VendedorRoutes as V_R
from src.routes.tienda.tienda_routes import TiendaRoutes as T_R
from src.routes.vendedor_tienda.vendedor_tienda_routes import VendedorTiendaRoutes as V_T_R

from src.controllers.ciudad.ciudad_controller import CiudadController as CI_C
from src.controllers.cliente.cliente_controller import ClienteController as C_C
from src.controllers.cliente_segmento.cliente_segmento_controller import ClienteSegmentoController as C_S_C
from src.controllers.gerente.gerente_controller import GerenteController as G_C
from src.controllers.region.region_controller import RegionController as R_C
from src.controllers.vendedor.vendedor_controller import VendedorController as V_C
from src.controllers.tienda.tienda_controller import TiendaController as T_C
from src.controllers.vendedor_tienda.vendedor_tienda_controller import VendedorTiendaController as V_T_C
class AppInitializer:
    def __init__(self,app,db,models):
        """
        Inicializa las rutas de la aplicación con la instancia de Flask proporcionada."""
        self.app=app
        self.routes()
        self.controllers(db,models)
    def getCiudadControllers(self):
        return self.ciudad_controllers
    def getClienteControllers(self):
        return self.cliente_controllers
    def getClienteSegmentoControllers(self):
        return self.cliente_segmento_controllers
    def getGerenteControllers(self):
        return self.gerente_controllers
    def getRegionControllers(self):
        return self.region_controllers
    def getVendedorControllers(self):
        return self.vendedor_controllers
    def getTiendaControllers(self):
        return self.tienda_controllers
    def getVendedorTiendaControllers(self):
        return self.vendedor_tienda_controllers
    def routes(self):
        self.ciudad_routes=CI_R(self.app,self)
        self.cliente_routes=C_R(self.app,self)
        self.cliente_segmento_routes=C_S_R(self.app,self)
        self.gerente_routes=G_R(self.app,self)
        self.region_routes=R_R(self.app,self)
        self.vendedor_routes=V_R(self.app,self)
        self.tienda_routes=T_R(self.app,self)
        self.vendedor_tienda_routes=V_T_R(self.app,self)
    def controllers(self,db,models):
        self.ciudad_controllers=CI_C(db,models)
        self.cliente_controllers=C_C(db,models)
        self.cliente_segmento_controllers=C_S_C(db,models)
        self.gerente_controllers=G_C(db,models)
        self.region_controllers=R_C(db,models)
        self.vendedor_controllers=V_C(db,models)
        self.tienda_controllers=T_C(db,models)
        self.vendedor_tienda_controllers=V_T_C(db,models)