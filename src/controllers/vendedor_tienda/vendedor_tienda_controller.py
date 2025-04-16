from flask import request
class VendedorTiendaController:
    def __init__(self,db,models):
        self.models=models
        self.db=db
    def getDb(self):
        return self.db
    def post_vendedor_tienda(self,data):
        data=request.json()
        vendedor_key=data['vendedor_key']
        tienda_key=data['tienda_key']
        if not vendedor_key or not tienda_key:
            return {
                "message": "'vendedor_key' y tienda_key' son requeridos."
            }
        else:
            new_vendedor_tienda=self.models.DIM_VENDEDOR_TIENDA(
                vendedor_key=vendedor_key,
                tienda_key=tienda_key
            )
        try:
            self.getDb().session.add(new_vendedor_tienda)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return{
                "message": f"Error al vendedor_tienda: {str(e)}"
            },500
    def get_vendedor_tienda(self):
        page=request.args.get('page',default=1,type=int)
        per_page=request.args.get('per_page',default=10,type=int)
        
        all_vendedor_tienda=self.models.DIM_GERENTE.query.paginate(page=page,per_page=per_page,error_out=False)
        if not all_vendedor_tienda.items:
            return {
                "message": "No hay vendedor_tienda registrados."
            },404
        else:
            return{
                "vendedor_tienda": [vendedor_tienda.to_dict() for vendedor_tienda in all_vendedor_tienda.items],
                "total": all_vendedor_tienda.total,
                "pagina_actual": all_vendedor_tienda.page,
                "total_paginas": all_vendedor_tienda.pages
            },200
    def put_vendedor_tienda(self,id,data):
        vendedor_tienda=self.models.DIM_VENDEDOR_TIENDA.query.filter_by(id=id)
        if not vendedor_tienda:
            return {
                "message": "No se ha encontrado con el gerente con el id requerido."
            },404
        if not data['fecha_renuncia']:
            return {
                "message": "El atributo 'fecha_renuncia' es requerido."
            },400
        else:
            vendedor_tienda.fecha_renuncia=data['fecha_renuncia']
            vendedor_tienda.activo=False
            try:
                self.getDb().session.add(vendedor_tienda)
                self.getDb().session.commit()
            except Exception as e:
                self.getDb().session.rollback()
                return{
                    "message": f"Error al guardar los cambios {str(e)}"
                },500
        return {
            "activo": vendedor_tienda.activo
        },200
    def get_vendedor_tienda_id(self,id):
        vendedor_tienda=self.models.DIM_VENDEDOR_TIENDA.query.filter_by(id=id)
        if not vendedor_tienda:
            return {
                "message": "Vendedor_tienda no encontrado por el id requerido."
            },400
        else:
            return{
                "vendedor":vendedor_tienda.vendedor,
                "tienda": vendedor_tienda.tienda
            }