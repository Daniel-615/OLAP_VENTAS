from flask import request,jsonify
class RegionController:
    def __init__(self,db,models):
        self.db=db
        self.models=models
    def getDb(self):
        return self.db
    def post_region(self,data):
        region_nombre=data.get('region_nombre')
        if not region_nombre:
            return jsonify({
                "message": "'region_nombre' es requerido."
            })
        else:
            new_region=self.models.DIM_REGION(
                region_nombre=region_nombre
            )
        try:
            self.getDb().session.add(new_region)
            self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({
                "message": f"Error al crear la region: {str(e)}"
            }),500
        return jsonify({
            "message": "Region creada correctamente"
        }),201
    def get_region(self):
        page=request.args.get('page',default=1,type=1)
        per_page=request.args.get('per_page',default=10,type=int)
        
        all_region=self.models.DIM_REGION.query.paginate(page=page,per_page=per_page,error_out=False)
        if not all_region.items:
            return jsonify({
                "message": "No hay regiones registradas."
            }),404
        else:
            return jsonify({
                "regiones":[regiones.to_dict() for regiones in all_region.items],
                "total": all_region.total,
                "pagina_actual": all_region.page,
                "total_paginas": all_region.pages
            }),200
    def put_region(self,id,data):
        region=self.models.DIM_REGION.query.filter_by(region_key=id).first()
        if not region:
            return jsonify({
                "message": "No se ha encontrado el region con el id requerido."
            }),404
        if not data.get('region_nombre'):
            return jsonify({
                "message": "El atributo 'region_nombre' es requerido."
            }),400
        region.region_nombre=data.get('region_nombre')
        try:
           self.getDb().session.add(region)
           self.getDb().session.commit()
        except Exception as e:
            self.getDb().session.rollback()
            return jsonify({
                "message": f"Error al guardar los cambios {str(e)}"
            }),500 
        return {
            "nombre": region.region_nombre 
        },200
    def get_region_id(self,id):
        region=self.models.DIM_REGION.query.filter_by(region_key=id).first()
        if not region:
            return {
                "message": "Region no encontrado por el id requerido."
            },404
        else:
            return jsonify({
                "nombre": region.region_nombre
            })