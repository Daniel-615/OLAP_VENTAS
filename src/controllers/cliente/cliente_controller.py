from flask import request
class ClienteController:
    def __init__(self,db,models):
        """
        Inicializa el controlador de cliente con el servicio proporcionado.
        """
        self.models=models
        self.db=db
    def getDb(self):
        return self.db
    def post_cliente(self,data):
        data = request.get_json()
        cliente_id=data['cliente_id']
        nombre=data['cliente_nombre']
        apellido=data['cliente_apellido']
        gmail=data['cliente_gmail']
        telefono=data['cliente_telefono']
        ciudad_id=data['ciudad_id']
        region_id=data['region_id']
        if not cliente_id or not nombre:
            return {
                "message" : "'nombre' y 'client_id' requeridos."
                }
        if not apellido or not gmail:
            return{
                "message": "'apellido' y 'gmail' son requeridos."
            }
        if not telefono or not ciudad_id or not region_id:
            return{
                "message": "'telefono' , 'ciudad_id' y 'region_id' son requeridos."
            }
        else:
            previous_ciudad=self.models.DIM_CIUDAD.query.filter_by(ciudad_key=ciudad_id).first()
            previous_region=self.models.DIM_REGION.query.filter_by(region_key=region_id)
            new_client=self.models.DIM_CLIENTE(
                    cliente_id=cliente_id,
                    nombre=nombre,
                    apellido=apellido,
                    email=gmail,
                    telefono=telefono,
                    ciudad=previous_ciudad,
                    region=previous_region
                )
            try:
                self.getDb().session.add(new_client)
                self.getDb().session.commit()
            except Exception as e:
                self.getDb().session.rollback()
                return {
                    "message": f"Error al crear la ciudad: {str(e)}"
                    },500
    def get_cliente(self):
        page=request.args.get('page',default=1,type=int)
        per_page=request.args.get('per_page',default=10,type=int)

        all_cliente=self.models.DIM_CLIENTE.query.paginate(page=page,per_page=per_page,error_out=False)

        if not all_cliente.items:
            return{
                "message": "No hay clientes registrados."
            },404
        else:
            return{
                "clientes": [cliente.to_dict() for cliente in all_cliente.items],
                "total": all_cliente.total,
                "pagina_actual": all_cliente.total,
                "total_paginas": all_cliente.pages
            },200
    def put_cliente(self,id,data):
        cliente=self.models.DIM_CLIENTE.query.filter_by(cliente_key=id)
        if not cliente:
            return {
                "message": "No se ha encontrado el cliente con el id establecido."
            },404
        
        if not data['cliente_gmail'] or not data['cliente_ciudad'] or not data['cliente_telefono'] or not data['cliente_region']:
            return{
                "message": "'cliente_gmail', 'cliente_ciudad', 'cliente_telefono' y 'cliente_region' son requeridos. "
            },404
        cliente.email=data['cliente_gmail']
        cliente.ciudad=data['cliente_ciudad']
        cliente.region=data['cliente_region']
        cliente.telefono=data['cliente_telefono']

        #Guardar los campos
        try:
            self.getDb().session.add(cliente)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return {
                "message": f"Error al guardar los cambios: {str(e)}"
            },500
        return{
            "gmail": cliente.email,
            "ciudad": cliente.ciudad,
            "region": cliente.region,
            "telefono": cliente.telefono
        },200
    def get_cliente_id(self,id):
        cliente=self.models.DIM_CLIENTE.query.filter_by(cliente_key=id)
        if not cliente:
            return{
                "message": "Ciudad no encontrada por el id requerido."
            },404
        else:
            return{
                "nombre": cliente.nombre,
                "apellido": cliente.apellido
            }
        