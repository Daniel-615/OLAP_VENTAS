from flask import request,jsonify
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
        cliente_id=data.get('cliente_id')
        nombre=data.get('cliente_nombre')
        apellido=data.get('cliente_apellido')
        gmail=data.get('cliente_gmail')
        telefono=data.get('cliente_telefono')
        ciudad_id=data.get('ciudad_id')
        if not cliente_id or not nombre:
            return jsonify({
                "message" : "'cliente_nombre' y 'client_id' requeridos."
                })
        if not apellido or not gmail:
            return jsonify({
                "message": "'apellido' y 'gmail' son requeridos."
            })
        if not telefono or not ciudad_id:
            return jsonify({
                "message": "'cliente_telefono' , 'ciudad_id' son requeridos."
            })
        else:
            previous_ciudad=self.models.DIM_CIUDAD.query.filter_by(ciudad_key=ciudad_id).first()
            if not previous_ciudad:
                return jsonify({
                    "message": f"No se encontró una ciudad con el ID '{ciudad_id}'."
                }), 404
            new_client=self.models.DIM_CLIENTE(
                    cliente_id=cliente_id,
                    nombre=nombre,
                    apellido=apellido,
                    email=gmail,
                    telefono=telefono,
                    ciudad=previous_ciudad.ciudad_key,
                )
            try:
                self.getDb().session.add(new_client)
                self.getDb().session.commit()
            except Exception as e:
                self.getDb().session.rollback()
                return jsonify({
                    "message": f"Error al crear la ciudad: {str(e)}"
                    }),500
            return jsonify({
                "message": "Cliente creado correctamente",
                "cliente":{
                    "cliente_id": cliente_id,
                    "cliente_nombre": nombre
                }
            }),201
    def get_cliente(self):
        page=request.args.get('page',default=1,type=int)
        per_page=request.args.get('per_page',default=10,type=int)

        all_cliente=self.models.DIM_CLIENTE.query.paginate(page=page,per_page=per_page,error_out=False)

        if not all_cliente.items:
            return jsonify({
                "message": "No hay clientes registrados."
            }),404
        else:
            return{
                "clientes": [cliente.to_dict() for cliente in all_cliente.items],
                "total": all_cliente.total,
                "pagina_actual": all_cliente.total,
                "total_paginas": all_cliente.pages
            },200
    def put_cliente(self,id,data):
        cliente=self.models.DIM_CLIENTE.query.filter_by(cliente_key=id).first()
        if not cliente:
            return jsonify({
                "message": "No se ha encontrado el cliente con el id establecido."
            }),404
        
        if not data.get('cliente_gmail') or not data.get('cliente_ciudad') or not data.get('cliente_telefono') or not data.get('cliente_region'):
            return jsonify({
                "message": "'cliente_gmail', 'cliente_ciudad', 'cliente_telefono' y 'cliente_region' son requeridos. "
            }),404
        cliente.email=data.get('cliente_gmail')
        cliente.ciudad=data.get('cliente_ciudad')
        cliente.region=data.get('cliente_region')
        cliente.telefono=data['cliente_telefono']

        #Guardar los campos
        try:
            self.getDb().session.add(cliente)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({
                "message": f"Error al guardar los cambios: {str(e)}"
            }),500
        return jsonify({
            "gmail": cliente.email,
            "ciudad": cliente.ciudad,
            "region": cliente.region,
            "telefono": cliente.telefono
        }),200
    def get_cliente_id(self,id):
        cliente=self.models.DIM_CLIENTE.query.filter_by(cliente_key=id).first()
        if not cliente:
            return jsonify({
                "message": "Ciudad no encontrada por el id requerido."
            }),404
        else:
            return jsonify({
                "nombre": cliente.nombre,
                "apellido": cliente.apellido
            })
        