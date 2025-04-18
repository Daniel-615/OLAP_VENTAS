from flask import request,jsonify
class ClienteSegmentoController:
    def __init__(self,db,models):
        """
        Inicializa el controlador de cliente segmento con el servicio proporcionado.
        """ 
        self.models=models
        self.db=db
    def getDb(self):
        return self.db
    def post_cliente_segmento(self,data):
        data=request.get_json()
        segmento_key=data.get('segmento_key')
        cliente_key=data.get('cliente_key')
        if not cliente_key or not segmento_key:
            return jsonify({
                "message": "'cliente_key' y 'segmento_key' son requeridos."
            }) 
        else:
            previous_cliente=self.models.DIM_CLIENTE.query.filter_by(cliente_key=cliente_key).first()
            previous_segmento=self.models.DIM_SEGMENTO.query.filter_by(segmento_key=segmento_key).first()
            new_cliente_segmento=self.models.DIM_CLIENTE_SEGMENTO(
                cliente_key=previous_cliente,
                segmento_key=previous_segmento
            )
            try:
                self.getDb().session.add(new_cliente_segmento)
                self.getDb().session.commit()
            except Exception as e:
                self.getDb().session.rollback()
                return jsonify({
                    "message": f"Error al crear el cliente segmento: {str(e)}"
                }),500
    def get_cliente_segmento(self):
        page=request.args.get('page',default=1,type=int)
        per_page=request.args.get('per_page',default=10,type=int)
            
        all_cliente_segmento=self.models.DIM_CLIENTE_SEGMENTO.query.paginate(page=page,per_page=per_page,error_out=False)

        if not all_cliente_segmento.items:
            return jsonify({
                "message": "No hay clientes segmento registrados."
            }),404
        else:
            return jsonify({
                "clientes_segmento": [cliente_segmento.to_dict() for cliente_segmento in all_cliente_segmento.items],
                "total": all_cliente_segmento.total,
                "pagina_actual": all_cliente_segmento.page,
                "total_paginas": all_cliente_segmento.pages
            }),200
    def put_cliente_segmento(self,id,data):
        cliente_segmento=self.models.DIM_CLIENTE.query.filter_by(cliente_segmento_key=id).first()  
        if not cliente_segmento:
            return jsonify({
                "message": "No se ha encontrado el cliente con el id establecido."
            }),404
        if not data.get('segmento_key'):
            return jsonify({
                "message": "El atributo 'segmento_key' es requerido."
            }),400
        cliente_segmento.segmento_key=data.get('segmento_key')
        try:
            self.getDb().session.add(cliente_segmento)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({
                "message": f"Error al guardar los cambios: {str(e)}"
            }),500
        return jsonify({
            "nombre": cliente_segmento.segmento_key
        }),200
    def get_cliente_segmento_id(self,id):
        cliente_segmento=self.models.DIM_CLIENTE_SEGMENTO.query.filter_by(cliente_segmento=id).first()
        if not cliente_segmento:
            return jsonify({
                "message": "Cliente segmento no encontrado por el id requerido."
            }),404
        else:
            return jsonify({
                "segmento_key": cliente_segmento.segmento_key,
                "cliente_key": cliente_segmento.cliente_key
            })
        
        
        