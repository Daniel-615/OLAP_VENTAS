from src.models.models import Models
from flask import request
class ClienteSegmentoController:
    def __init__(self,db):
        """
        Inicializa el controlador de cliente segmento con el servicio proporcionado.
        """
        self.models=Models(db)
        self.db=db
    def getDb(self):
        return self.db
    def post_cliente_segmento(self,data):
        segmento_key=data.segmento_key
        cliente_key=data.cliente_key
        if not cliente_key or not segmento_key:
            return{
                "message": "'cliente_key' y 'segmento_key' son requeridos."
            } 
        else:
            previous_cliente=self.models.DIM_CLIENTE.query.filter_by(cliente_key=cliente_key)
            previous_segmento=self.models.DIM_SEGMENTO.query.filter_by(segmento_key=segmento_key)
            new_cliente_segmento=self.models.DIM_CLIENTE_SEGMENTO(
                cliente_key=previous_cliente,
                segmento_key=previous_segmento
            )
            try:
                self.getDb().session.add(new_cliente_segmento)
                self.getDb().session.commit()
            except Exception as e:
                self.getDb().session.rollback()
                return {
                    "message": f"Error al crear la ciudad: {str(e)}"
                },500
    def get_cliente_segmento(self):
        page=request.args.get('page',default=1,type=int)
        per_page=request.args.get('per_page',default=10,type=int)
            
        all_cliente_segmento=self.models.DIM_CLIENTE_SEGMENTO.query.paginate(page=page,per_page=per_page,error_out=False)

        if not all_cliente_segmento.items:
            return{
                "message": "No hay clientes segmento registrados."
            },404
        else:
            return{
                "clientes_segmento": [cliente_segmento.to_dict() for cliente_segmento in all_cliente_segmento.items],
                "total": all_cliente_segmento.total,
                "pagina_actual": all_cliente_segmento.total,
                "total_paginas": all_cliente_segmento.pages
            },200
    def put_cliente_segmento(self,id,data):
        cliente_segmento=self.models.DIM_CLIENTE.query.filter_by(cliente_segmento_key=id)   
        if not cliente_segmento:
            return {
                "message": "No se ha encontrado el cliente con el id establecido."
            },404
        
        