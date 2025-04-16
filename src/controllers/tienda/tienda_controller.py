from flask import request
class TiendaController:
    def __init__(self,db,models):
        self.models=models
        self.db=db
    def getDb(self):
        return self.db
    def post_tienda(self,data):
        data=request.json()
        tienda_id=data['tienda_id']
        nombre_tienda=data['nombre_tienda']
        direccion=data['direccion']
        ciudad=data['ciudad']
        region=data['region']
        tamaño_m2=data['tamaño_m2']
        horario_apertura=data['horario_apertura']
        horario_cierre=data['horario_cierre']
        if not tienda_id or not nombre_tienda or not direccion or not ciudad or not region or not tamaño_m2 or not horario_apertura or not horario_cierre:
            return {
                "message": "'tienda_id', 'nombre_tienda', 'direccion', 'ciudad','region','tamaño_m2', 'horario_apertura' y 'horario_cierre' son requeridos."
            }
        else:
            new_tienda=self.models.DIM_TIENDA(
                tienda_id=tienda_id,
                nombre_tienda=nombre_tienda,
                direccion=direccion,
                ciudad=ciudad,
                region=region,
                tamaño_m2=tamaño_m2,
                horario_apertura=horario_apertura,
                horario_cierre=horario_cierre
            )
        try:
            self.getDb().session.add(new_tienda)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return {
                "message": f"Error al crear la tienda: {str(e)}"
            },500
    def get_tienda(self):
        page=request.args.get('page',default=1,type=int)
        per_page=request.args.get('per_page',default=10,type=int)

        all_tienda=self.models.DIM_TIENDA.query.paginate(page=page,per_page=per_page,error_out=False)
        if not all_tienda.items:
            return{
                "message": "No hay tiendas registradas."
            },404
        else:
            return{
                "tiendas": [tiendas.to_dict() for tiendas in all_tienda.items],
                "total": all_tienda.total,
                "pagina_actual": all_tienda.page,
                "total_paginas": all_tienda.pages
            },200
    def put_tienda(self,id,data):
        tienda=self.models.DIM_TIENDA.query.filter_by(tienda_key=id)
        if not tienda:
            return{
                "message": "No se ha encontrado la tienda con el id requerido."
            }
        if not data['horario_apertura'] or not data['horario_cierre']:
            return{
                "message": "El atributo 'horario_apertura' y el 'horario_cierre' son requeridos."
            },400
        tienda.horario_apertura=data['horario_apertura']
        tienda.horario_cierre=data['horario_cierre']
        try:
            self.getDb().session.add(tienda)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return {
                "message": f"Error al guardar los cambios {str(e)}"
            }
        return{
            "horario_apertura": tienda.horario_apertura,
            "horario_cierre": tienda.horario_cierre
        },200
    
    def get_tienda_id(self,id):
        tienda=self.models.DIM_TIENDA.query.filter_by(tienda_key=id)
        if not tienda:
            return {
                "message": "Tienda no encontrada por el id requerido."
            },404
        else:
            return{
                "nombre_tienda": tienda.nombre_tienda,
                "horario_apertura": tienda.horario_apertura,
                "horario_cierre": tienda.horario_cierre
            }