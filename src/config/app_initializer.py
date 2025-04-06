from src.routes.ciudad.ciudad_routes import CiudadRoutes as CI_R
from src.routes.cliente.cliente_routes import ClienteRoutes as C_R
from src.routes.cliente_segmento.cliente_segmento_routes import ClienteSegmentoRoutes as C_S_R
from src.routes.gerente.gerente_routes import GerenteRoutes as G_R
from src.routes.region.region_routes import RegionRoutes as R_R
from src.routes.vendedor.vendedor_routes import VendedorRoutes as V_R
from src.routes.tienda.tienda_routes import TiendaRoutes as T_R
from src.routes.vendedor_tienda.vendedor_tienda_routes import VendedorTiendaRoutes as V_T_R
class AppInitializer:
    def __init__(self,app):
        """
        Inicializa las rutas de la aplicación con la instancia de Flask proporcionada."""
        self.app=app
        self.ciudad_routes=CI_R(self.app)
        self.cliente_routes=C_R(self.app)
        self.cliente_segmento_routes=C_S_R(self.app)
        self.gerente_routes=G_R(self.app)
        self.region_routes=R_R(self.app)
        self.vendedor_routes=V_R(self.app)
        self.tienda_routes=T_R(self.app)
        self.vendedor_tienda_routes=V_T_R(self.app)
