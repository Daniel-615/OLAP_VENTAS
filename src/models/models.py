from sqlalchemy.dialects.postgresql import UUID
import uuid

class Models:
    def __init__(self, db):
        self.db = db

        class DIM_GERENTE(db.Model):
            __tablename__ = 'DIM_GERENTE'
            __table_args__ = {'extend_existing': True}
            gerente_key = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
            gerente_id = db.Column(db.String(50), nullable=False, unique=True)
            nombre = db.Column(db.String(30), nullable=False)
            def to_dict(self):
                return {'nombre': self.nombre}
        self.DIM_GERENTE = DIM_GERENTE
        
        class DIM_REGION(db.Model):
            __tablename__ = 'DIM_REGION'
            __table_args__ = {'extend_existing': True}
            region_key = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
            region_nombre = db.Column(db.String(100), nullable=False, unique=True)
            def to_dict(self):
                return {'region_nombre': self.region_nombre}
        self.DIM_REGION = DIM_REGION

        class DIM_CIUDAD(db.Model):
            __tablename__ = 'DIM_CIUDAD'
            __table_args__ = {'extend_existing': True}
            ciudad_key = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
            ciudad_nombre = db.Column(db.String(100), nullable=False, unique=True)
            region_key = db.Column(UUID(as_uuid=True), db.ForeignKey('DIM_REGION.region_key'), nullable=False)
            def to_dict(self):
                return {'ciudad_nombre': self.ciudad_nombre, 'region_key': self.region_key}
        self.DIM_CIUDAD = DIM_CIUDAD

        class DIM_SEGMENTO(db.Model):
            __tablename__ = 'DIM_SEGMENTO'
            __table_args__ = {'extend_existing': True}
            segmento_key = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
            segmento_id = db.Column(db.String(50), nullable=False, unique=True)
            nombre = db.Column(db.String(30), nullable=False)
            def to_dict(self):
                return {'nombre': self.nombre}
        self.DIM_SEGMENTO = DIM_SEGMENTO

        class DIM_CLIENTE(db.Model):
            __tablename__ = 'DIM_CLIENTE'
            __table_args__ = (
                db.UniqueConstraint('nombre', 'apellido', 'email', name='uq_nombre_apellido_email'),
                {'extend_existing': True}
            )
            cliente_key = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
            cliente_id = db.Column(db.String(50), nullable=False, unique=True)
            nombre = db.Column(db.String(30), nullable=False)
            apellido = db.Column(db.String(30), nullable=False)
            email = db.Column(db.String(50), nullable=False, unique=True)
            telefono = db.Column(db.String(20), nullable=False, unique=True)
            ciudad = db.Column(UUID(as_uuid=True),db.ForeignKey('DIM_CIUDAD.ciudad_key'), nullable=False)
            region = db.Column(UUID(as_uuid=True),db.ForeignKey('DIM_REGION.region_key'), nullable=False)
            fecha_registro = db.Column(db.Date, nullable=False)
            def to_dict(self):
                return {
                    'nombre': self.nombre,
                    'apellido': self.apellido,
                    'email': self.email
                }
        self.DIM_CLIENTE = DIM_CLIENTE

        class DIM_CLIENTE_SEGMENTO(db.Model):
            __tablename__ = 'DIM_CLIENTE_SEGMENTO'
            __table_args__ = {'extend_existing': True}
            cliente_segmento_key = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
            cliente_key = db.Column(UUID(as_uuid=True), db.ForeignKey('DIM_CLIENTE.cliente_key'), nullable=False)
            segmento_key = db.Column(UUID(as_uuid=True), db.ForeignKey('DIM_SEGMENTO.segmento_key'), nullable=False)
            def to_dict(self):
                return {
                    'cliente_key': self.cliente_key,
                    'segmento_key': self.segmento_key
                }
        self.DIM_CLIENTE_SEGMENTO = DIM_CLIENTE_SEGMENTO

        class DIM_TIENDA(db.Model):
            __tablename__ = 'DIM_TIENDA'
            __table_args__ = (
                db.UniqueConstraint('nombre_tienda', 'direccion', 'ciudad', name='uq_nombre_direccion_ciudad'),
                db.CheckConstraint('tamaño_m2 > 0', name='ck_tamaño_m2_positive'),
                db.CheckConstraint('horario_apertura < horario_cierre', name='ck_horario_apertura_cierre'),
                {'extend_existing': True}
            )
            tienda_key = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
            tienda_id = db.Column(db.String(50), nullable=False, unique=True)
            nombre_tienda = db.Column(db.String(100), nullable=False)
            direccion = db.Column(db.String(200), nullable=False)
            ciudad = db.Column(UUID(as_uuid=True),db.ForeignKey('DIM_CIUDAD.ciudad_key'), nullable=False)
            region = db.Column(UUID(as_uuid=True),db.ForeignKey('DIM_REGION.region_key'), nullable=False)
            tamaño_m2 = db.Column(db.Float, nullable=False)
            fecha_apertura = db.Column(db.Date, nullable=False)
            horario_apertura = db.Column(db.Time, nullable=False)
            horario_cierre = db.Column(db.Time, nullable=False)
            def to_dict(self):
                return {
                    'nombre_tienda': self.nombre_tienda,
                    'direccion': self.direccion,
                    'ciudad': self.ciudad,
                    'region': self.region
                }
        self.DIM_TIENDA = DIM_TIENDA

        class DIM_VENDEDOR(db.Model):
            __tablename__ = 'DIM_VENDEDOR'
            __table_args__ = (
                db.UniqueConstraint('vendedor_id', name='uq_vendedor_id'),
                db.CheckConstraint('edad > 0', name='ck_edad_positive'),
                db.CheckConstraint('salario > 0', name='ck_salario_positive'),
                {'extend_existing': True}
            )
            vendedor_key = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
            vendedor_id = db.Column(db.String(50), nullable=False, unique=True)
            nombre = db.Column(db.String(30), nullable=False)
            edad = db.Column(db.Integer, nullable=False)
            salario = db.Column(db.Float, nullable=False)
            activo = db.Column(db.Boolean, nullable=False)
            def to_dict(self):
                return {
                    'nombre': self.nombre,
                    'edad': self.edad,
                    'salario': self.salario
                }
        self.DIM_VENDEDOR = DIM_VENDEDOR

        class VENDEDOR_TIENDA(db.Model):
            __tablename__ = 'VENDEDOR_TIENDA'
            id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
            vendedor_key = db.Column(UUID(as_uuid=True), db.ForeignKey('DIM_VENDEDOR.vendedor_key'), nullable=False)
            tienda_key = db.Column(UUID(as_uuid=True), db.ForeignKey('DIM_TIENDA.tienda_key'), nullable=False)
            fecha_contratacion = db.Column(db.Date, nullable=False)
            fecha_renuncia = db.Column(db.Date, nullable=True)
            activo = db.Column(db.Boolean, nullable=False)
            __table_args__ = (
                db.CheckConstraint('fecha_renuncia IS NULL OR fecha_renuncia > fecha_contratacion', name='ck_fecha_renuncia_valida'),
                {'extend_existing': True}
            )
        self.VENDEDOR_TIENDA = VENDEDOR_TIENDA

    def getDB(self):
        return self.db